import discord
from database import connexion
import constants.sql_request as requests
import constants.messages as messages
from aiosqlite import Cursor
from bot_class import ArgoBot



### Statistiques
class EmbedStatPlongeur(discord.Embed):
    def __init__(self):
        super().__init__(
            title="Statistiques",
            color=discord.Colour.orange(),
            type="rich"
        )


    
    async def set_stats(self):
        conn = await connexion()
        cur = await conn.cursor()

        self.nb_plongeurs = int((await (await cur.execute(requests.COUNT_PLONGEUR)).fetchone())[0])

        self.description = "Les statistiques concernent seulement les plongeurs enregistrés dans la base de donnée."
        self.description += f"\nIl y a `{self.nb_plongeurs}` plongeurs enregistrés."
        
        await self.__stat_federations(cur)

        await cur.close()
        await conn.close()
    


    async def __stat_federations(self, cur: Cursor):
        nb_ffessm = int((await (await cur.execute(requests.COUNT_FFESSM)).fetchone())[0])
        nb_padi = int((await (await cur.execute(requests.COUNT_PADI)).fetchone())[0])
        nb_ssi= int((await (await cur.execute(requests.COUNT_SSI)).fetchone())[0])
        
        fede = messages.STATS_PLONGEUR_FEDE.format(
            ffessm_count = nb_ffessm,
            ffessm_percentage = 100 * nb_ffessm / self.nb_plongeurs,
            padi_count = nb_padi,
            padi_percentage = 100 * nb_padi / self.nb_plongeurs,
            ssi_count = nb_ssi,
            ssi_percentage = 100 * nb_ssi / self.nb_plongeurs
        )

        self.add_field(
            name="Fédérations:",
            value=fede
        )
    

# Affiche toutes les informations concernant un plongeur
class EmbedPlongeur(discord.Embed):
    avatar_url = None

    def __init__(self, bot: ArgoBot, idPlongeur: int):
        super().__init__()
        self.bot = bot
        self.idPlongeur = idPlongeur

        
        
    async def build(self):
        if self.fields:
            return
        
        conn = await connexion()
        cur = await conn.cursor()

        # Données table plongeur
        plongeur = (await (await cur.execute(requests.SELECT_PLONGEUR, (self.idPlongeur, ))).fetchall())[0]
        prenom = plongeur[1]
        nombre_plongee = plongeur[2]
        region = plongeur[3]
        description = plongeur[4]
        pratique = [0, 1] if plongeur[5] == 2 else [plongeur[5]]


        self.title = prenom
        self.description = f"{region}, moins de `{nombre_plongee}` plongées"
        self.color = int('0x0080FF', base=16)

        req_fede = requests.SELECT_SIGLE_FEDE.format(self.idPlongeur)
        req_niv = requests.SELECT_NOM_NIVEAU.format(self.idPlongeur)
        req_spe = requests.SELECT_NOM_SPECIALITE.format(self.idPlongeur)
        req_interet = requests.SELECT_NOM_INTERET.format(self.idPlongeur)

        fede = list()
        niveaux = list()
        specialites = list()
        interets = list()

        to_read = [fede, niveaux, specialites, interets]
        all_req = [req_fede, req_niv, req_spe, req_interet]
        for donnee, req in zip(to_read, all_req):
            result = await (await cur.execute(req)).fetchall()
            for r in result:
                donnee.append(r[0])
        
        # Si le plongeur est professionnel on affiche ses activités pros
        activites_pro = []
        if plongeur[5] == "1" or plongeur[5] == "2":
            req_activite_pro = requests.SELECT_NOM_ACTIVITE_PRO.format(self.idPlongeur)
            result = await (await cur.execute(req_activite_pro)).fetchall()
            for r in result:
                activites_pro.append(r[0])
        
        await cur.close()
        await conn.close()

        
        self.add_field(
            name="Fédérations",
            value=", ".join(fede),
            inline=False
        )

        self.add_field(
            name="Niveaux",
            value=", ".join(niveaux),
            inline=False
        )

        self.add_field(
            name="Spécialités",
            value=", ".join(specialites),
            inline=False
        )

        self.add_field(
            name="Intérêts",
            value=", ".join(interets),
            inline=False
        )

        if activites_pro:
            self.add_field(
                name="Activités Professionnelles",
                value=", ".join(activites_pro)
            )

        self.add_field(
            name="Description",
            value=description,
            inline=False
        )

        await self.set_avatar()
        
        return self



    async def set_avatar(self):
        if self.avatar_url == None:
            self.avatar_url = (await self.bot.get_or_fetch_user(self.idPlongeur)).display_avatar.url

            # Au cas où erreur lors de la récupération de l'avatar
            if self.avatar_url != None: self.set_thumbnail(url=self.avatar_url)
