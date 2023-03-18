import discord
from database import connexion
import constants.sql_request as requests
import constants.messages as messages
from aiosqlite import Cursor



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
    