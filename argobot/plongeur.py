import discord
import database
import json
from diver_card import create_diver_card
import constants.sql_request as sql_request

from static_data import InfoGenerique, NiveauPlongee
from globals import global_data
import io


# Classe représentant un plongeur

class Plongeur():
    def __init__(self, user: discord.Member) -> None:
        self.user = user

        self.federations: list[InfoGenerique] = []
        self.niveaux: list[NiveauPlongee] = []
        self.nombre_plongee: int = 0
        self.specialites: list[InfoGenerique] = []
        self.pratique: str = ""
        self.interets: list[InfoGenerique] = []
        self.professions: list[InfoGenerique] = []
        self.prenom: str = ''
        self.region: str = ''
        self.description: str = ''
        self.search_consent = False
        self.pratique_str = ""

        self.all_infos = [self.federations, self.niveaux, self.specialites, self.interets, self.professions]


    async def est_dans_db(self):
        """Renvoie True si le plongeur est dans la base de données, False sinon"""
        conn = await database.connexion()
        cur = await conn.cursor()

        req = "SELECT * FROM Plongeur WHERE idPlongeur = ?;"
        result = bool(await (await cur.execute(req, [self.user.id])).fetchall())
        
        await cur.close()
        await conn.close()
        return result
            


    async def supprime(self):
        """Supprime le plongeur de la base de données"""
        conn = await database.connexion()

        # Suppression en cascade sur les tables liés à l'idPlongeur
        req = "DELETE FROM Plongeur WHERE idPlongeur = ?;"
        await conn.execute(req, (self.user.id, ))

        await conn.commit()
        await conn.close()



    async def load_from_db(self, force_reload=False):
        """
        Charge les données depuis la base de donnée au lieu de les demander via le menu.
        Si le plongeur n'est pas dans la base de données, retourne None
        """
        # évite de réinterroger la base de données pour rien
        if self.prenom and not force_reload:
            return self


        conn = await database.connexion()
        cur = await conn.cursor()

        id = self.user.id

        plongeur = await (await cur.execute(sql_request.SELECT_PLONGEUR, (id, ))).fetchall()
        
        # Si le plongeur n'est pas dans la base de données
        if not plongeur:
            await cur.close()
            await conn.close()
            return None    

        plongeur = plongeur[0]    

        # Données table plongeur
        self.prenom = plongeur[1]
        self.nombre_plongee = plongeur[2]
        self.region = plongeur[3]
        self.description = plongeur[4]
        self.pratique = [0, 1] if plongeur[5] == "2" else [plongeur[5]]
        self.search_consent = bool(plongeur[6])

        if len(self.pratique) == 2:
            self.pratique_str = "Loisir & Professionnelle"
        else:
            self.pratique_str = "Loisir" if self.pratique[0] == "0" else "Professionnelle"


        # Autres tables
        for donnee, info in zip(self.all_infos, global_data.all_infos_str):
            req = sql_request.SELECT_PLONGEUR_POSSEDE_INFO.format(info=info)
            result = await (await cur.execute(req, (id, ))).fetchall()
            for r in result:
                donnee.append(global_data.get_info(info, r[0]))

        await cur.close()
        await conn.close()

        return self



    async def to_db(self):
        """
        Insère le plongeur dans la base de données (ou met à jour les informations s'il
        est déjà dedans).
        On utilise l'identifiant Discord (entier non signé sur 64 bits) comme identifiant d'un 
        utilisateur
        """
        conn = await database.connexion()
        cur = await conn.cursor()

        # Si le plongeur est déjà dans la DB on le supprime pour mettre à jour
        if await self.est_dans_db():
            await self.supprime()
            

        data = dict()

        # Table Plongeur
        data['idPlongeur'] = self.user.id
        data['prenom'] = self.prenom
        data['nombrePlongees'] = self.nombre_plongee
        data['region'] = self.region
        data['description'] = self.description
        data['pratique'] = self.pratique[0] if len(self.pratique) != 2 else 2   # ! 
        data['consent'] = int(self.search_consent)          # Pas de bool avec SQLite
        await cur.execute(sql_request.INSERT_PLONGEUR, data)

        # Autres tables (PlongeurPossede...)
        to_insert = [self.federations, self.niveaux, self.specialites, self.interets, self.professions]
        for donnee, info in zip(to_insert, global_data.all_infos_str):     
            if donnee:
                req = sql_request.INSERT_PLONGEUR_POSSEDE_INFO.format(info=info)
                params = [(self.user.id, x.id) for x in donnee]
                await cur.executemany(req, params)

        await conn.commit()
        await cur.close()
        await conn.close()


    
    async def get_card(self) -> discord.File:
        """
        Retourne l'image de la carte du plongeur
        """
        if not (await self.load_from_db()):
            return None
        
        
        with io.BytesIO() as img_bytes:
            create_diver_card(self, img_bytes)
            img_bytes.seek(0)
            result = discord.File(fp=img_bytes, filename=f"{self.prenom}.jpg")

        return result
    


    async def to_json(self) -> str:
        """
        Retourne un string représentant les informations au format JSON
        Utilisé pour produire un fichier JSON pour les RGPD
        (L'utilisateur doit avoir accès à une version de ses données traitable automatiquement)
        """
        # On suppose que le plongeur est dans la base de données
        if not (await self.load_from_db()):
            return None
        
        
        result = dict()
        result["IdentifiantDiscord"] = self.user.id
        result["PrenomOuPseudo"] = self.prenom
        result["NombrePlongees"] = self.nombre_plongee
        result["Region"] = self.region
        result["Description"] = self.description
        result["Pratique"] = self.pratique_str
        result["ConsentementResultatsRecherche"] = self.search_consent

        result["Federations"] = [x.nom for x in self.federations]
        result["Niveaux"] = [x.nom for x in self.niveaux]
        result["Specialites"] = [x.nom for x in self.specialites]
        result["Interets"] = [x.nom for x in self.interets]
        result["ProfessionsPlongee"] = [x.nom for x in self.professions]

        return json.dumps(result, indent=4, ensure_ascii=False)
    


    async def to_embed(self) -> discord.Embed:
        """
        Retourne un discord.Embed résumant toutes les informations du plongeur.
        """
        if not (await self.load_from_db()):
            return None
        
        result = discord.Embed()
        result.title = self.prenom
        result.description = f"**Région**: {self.region}\nMoins de `{self.nombre_plongee}` plongées"
        result.color = int('0x0080FF', base=16)
        result.set_thumbnail(url=self.user.display_avatar.url)
        result.set_footer(text=f"Identifiant Discord: {self.user.id}")

        for info, info_str in zip(self.all_infos, global_data.all_infos_pretty):
            if info_str == "Professions":
                result.add_field (
                    name="Pratique de la plongée",
                    value=self.pratique_str,
                    inline=False
                )
                if not info:
                    # Rien à afficher pour les professions
                    continue

            result.add_field (
                name=info_str,
                value=', '.join([x.nom for x in info]),
                inline=False
            )
        
        # La description peut contenir 4096 caractères mais la value d'un champ d'embed ne peut
        # contenir que 1024 caractères.
        # On sépare donc en plusieurs champs
        tmp_desc = self.description[:1024]
        i = 1
        while tmp_desc:
            result.add_field (
                name="Description" if i == 1 else "",
                value=tmp_desc,
                inline=False
            )
            tmp_desc = self.description[i * 1024:(i + 1) * 1024]
            i += 1

        return result

        

    # todo: remettre au bon endroit (menu de creation)
    def reset_menu1(self):
        self.federations = []
        self.niveaux = []
        self.nombre_plongee = 0
        self.specialites = []
    

    def reset_menu2(self):
        self.pratique = []
        self.interets = []
        self.professions = []
        self.search_consent = False
    

    def menu1_est_complet(self):
        """
        Retourne True si les informations demandées dans le
        premier menu sont *toutes* renseignées, False sinon
        """
        return self.federations and self.niveaux and self.nombre_plongee and self.specialites

    def menu2_est_complet(self):
        """
        Retourne True si les informations demandées dans le
        deuxième menu sont *toutes* renseignées, False sinon
        """
        if 1 in self.pratique:  # Si le plongeur est professionnel on prend en compte la profession
            return self.pratique and self.interets and self.professions

        return self.pratique and self.interets
