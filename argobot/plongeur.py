import io
import discord
import database
from diver_card import create_diver_card
import constants.sql_request as sql_request
import constants.select_options as options


# Classe représentant un plongeur

class Plongeur():
    def __init__(self, user: discord.Member) -> None:
        self.user = user


        self.federations: list[int] = []
        self.niveaux: list[int] = []
        self.nombre_plongee: int = 0
        self.specialites: list[int] =  []
        self.pratique: list[int] = []
        self.interets: list[int] = []
        self.profession: list[int] = []
        self.prenom: str = ''
        self.region: str = ''
        self.description: str = ''
        self.search_consent = False

        

    async def est_dans_db(self):
        """Renvoie True si le plongeur est dans la base de données, False sinon"""
        conn = await database.init_bd()
        cur = await conn.cursor()

        result = bool(await (await cur.execute("SELECT * FROM Plongeur WHERE idPlongeur = ?", [self.user.id])).fetchall())
        
        await cur.close()
        await conn.close()
        return result
            


    async def supprime(self):
        """Supprime le plongeur de la base de données"""
        conn = await database.init_bd()
        cur = await conn.cursor()

        for request in sql_request.DELETE_REQUESTS:
                await cur.execute(request, (self.user.id, ))


        await conn.commit()
        await cur.close()
        await conn.close()



    async def envoi_carte(self, ctx: discord.ApplicationContext):
        """Envoie la carte du plongeur.
        
        La carte est seulement visible de la personne qui a réalisé la commande,
        et chaque personne ne peut accéder qu'à SA carte de plongeur. """
        fede = "ERROR"
        for f in options.FEDERATIONS:
            if f.value == str(self.federations[0]):
                fede = f.label
        
        niveau = "ERROR"
        for n in (options.NIVEAUX_FFESSM + options.NIVEAUX_PADI + options.NIVEAUX_SSI):
            if n.value == str(self.niveaux[0]):
                niveau = n.label
        
        niveauToAnimal = {'10': "Crevette", '20': "Méduse", '50': "Tortue", '100': "Homard",
                          '500': "Phoque", '1000': "Requin", '2000': "Orque", '5000': "Mégalodon"}

        # Supression d'éventuels emoji
        new_str = ""
        for c in self.prenom:
            # Pour éviter les caractères non ASCII comme les emojis (pas supportés par la police)
            if ord(c) <= 255:   
                new_str += c
        self.prenom = new_str
            
        new_str = ""
        for c in self.region:
            if ord(c) <= 255:
                new_str += c
        self.region = new_str
        

        with io.BytesIO() as b_img:
            create_diver_card(self.prenom, self.region, fede, niveau, niveauToAnimal[str(self.nombre_plongee)], b_img)
            b_img.seek(0)

            await ctx.respond(file=discord.File(fp=b_img, filename=f"{self.prenom}.jpg"), ephemeral=True)




    async def load_from_db(self):
        """Charge les données depuis la base de donnée au lieu de les demander via le menu.
        
        Si le plongeur n'est pas dans la base de données, retourne None"""
        if not await self.est_dans_db():
            return None
        

        conn = await database.init_bd()
        cur = await conn.cursor()

        id = self.user.id

        # Données table plongeur
        plongeur = await (await cur.execute(sql_request.SELECT_PLONGEUR, (id, ))).fetchall()
        self.prenom = plongeur[0][1]
        self.nombre_plongee = plongeur[0][2]
        self.region = plongeur[0][3]
        self.description = plongeur[0][4]
        self.pratique = [0, 1] if plongeur[0][5] == 2 else [plongeur[0][5]]
        self.search_consent = bool(plongeur[0][6])


        # Autres tables
        to_read = [self.federations, self.niveaux, self.interets, self.specialites, self.profession]
        for donnee, req in zip(to_read, sql_request.SELECT_REQUESTS):
            result = await (await cur.execute(req, (id, ))).fetchall()
            for r in result:
                donnee.append(r[0])

        await cur.close()
        await conn.close()

        return self
    


    async def to_db(self):
        """Insère le plongeur dans la base de données (ou met à jour les informations s'il
        est déjà dedans).
        
        On utilise l'identifiant Discord (entier sur 18 chiffres) comme identifiant d'un utilisateur"""
        conn = await database.init_bd()
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
        data['consent'] = 1 if self.search_consent else 0       # Pas de bool en SQLite
        await cur.execute(sql_request.INSERT_PLONGEUR, data)

        # Autres tables
        to_insert = [self.federations, self.niveaux, self.interets, self.specialites, self.profession]
        for donnee, req in zip(to_insert, sql_request.INSERT_REQUESTS):     # ! Attention à l'ordre dans INSERT_REQUESTS
            if donnee:
                params = [(self.user.id, id) for id in donnee]
                await cur.executemany(req, params)

        await conn.commit()
        await cur.close()
        await conn.close()
    


    def reset_menu1(self):
        self.federations = []
        self.niveaux = []
        self.nombre_plongee = 0
        self.specialites = []
    

    def reset_menu2(self):
        self.pratique = []
        self.interets = []
        self.profession = []
        self.search_consent = False
    

    def menu1_est_complet(self):
        """Retourne True si les informations demandées dans le
        premier menu sont *toutes* renseignées, False sinon
        """
        return self.federations and self.niveaux and self.nombre_plongee and self.specialites

    def menu2_est_complet(self):
        """Retourne True si les informations demandées dans le
        deuxième menu sont *toutes* renseignées, False sinon
        """
        if 1 in self.pratique:  # Si le plongeur est professionnel on prend en compte la profession
            return self.pratique and self.interets and self.profession and self.search_consent

        return self.pratique and self.interets and self.search_consent
