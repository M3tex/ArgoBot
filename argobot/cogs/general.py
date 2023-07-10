import discord
from menus.recherche_binome import MenuRecherche
from menus.creation_infos_plongeur import MenuInfosStockees
import constants.messages as messages
from bot_class import ArgoBot
from plongeur import Plongeur

from discord.ext.commands import Cog, slash_command
from menus.meteo import MenuChoixVille, MeteoResult, _get_embed_from_city
from globals import CONSTANTES
import aiohttp



# Commandes ne faisant pas partie d'un sous-groupe.
#
# Actuellement:
# /rgpd
# /recherche_binome
# /meteo <ville> [complet: Oui|Non]


class GeneralCommands(Cog):
    
    def __init__(self, bot: ArgoBot):
        super().__init__()
        self.bot = bot
    

    @slash_command(name="rgpd", description="Informations sur les RGPD")
    async def rgpd(self, ctx: discord.ApplicationContext):
        plongeur = Plongeur(ctx.user)
        await ctx.respond(content=messages.RGPD, view=MenuInfosStockees(plongeur, self.bot), ephemeral=True)


    @slash_command(name = "recherche_binome", description = "Permet de rechercher un binome")
    async def recherche_binome(self, ctx: discord.ApplicationContext):
        view = MenuRecherche(ctx.bot)

        await ctx.respond(content=messages.RECHERCHE_BINOME, view=view, ephemeral=True)
        return


    @slash_command(name="meteo", description="Affiche la météo")
    @discord.option(
        name="lieu",
        type=str,
        required=True,
        description="Le lieu concerné (par exemple: Marseille)"
    )
    @discord.option(
        "complet",
        description="Prévisions heures par heures (non par défaut)",
        choices=["Oui", "Non"],
        required=False
    )
    async def meteo(self, ctx: discord.ApplicationContext, lieu: str, complet: str = "Non"):
        complet = complet == "Oui"
        
        # Pour récupérer la latitude / longitude avec le nom de la ville
        ans: dict = None
        req = f"https://geocoding-api.open-meteo.com/v1/search?name={lieu}&count=25&language=fr&format=json"
        async with aiohttp.ClientSession() as session:
            async with session.get(req) as response:
                ans = await response.json()
        

        # Pas de ville trouvée
        if not ans or len(ans) == 1:
            msg = CONSTANTES.messages.NO_RESULT_METEO.format(ville=lieu)
            await ctx.respond(content=msg, ephemeral=True)
            return
        
        # Si plusieurs résultats on laisse l'utilisateur choisir la bonne ville
        if len(ans["results"]) > 1:
            await ctx.respond(view=MenuChoixVille(ans['results'], complet), ephemeral=True)
        else:
            # Sinon on lance directement l'affichage des résultats
            tmp = lat = ans['results'][0]
            lat = tmp['latitude']
            long = tmp['longitude']
            name = tmp['name']
            cc = tmp['country_code']
            paginator = MeteoResult(await _get_embed_from_city(lat, long, name, cc, complet))

            await paginator.respond(ctx.interaction, ephemeral=True)



def setup(bot: ArgoBot):
    bot.add_cog(GeneralCommands(bot))