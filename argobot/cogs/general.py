import discord
from menus.recherche_binome import MenuRecherche
from menus.creation_infos_plongeur import MenuInfosStockees
import constants.messages as messages
from bot_class import ArgoBot
from plongeur import Plongeur

from discord.ext.commands import Cog, slash_command



# Commandes ne faisant pas partie d'un sous-groupe.
#
# Actuellement:
# /rgpd
# /recherche_binome


class GeneralCommands(Cog):
    
    def __init__(self, bot: ArgoBot):
        super().__init__()
        self.bot = bot
    

    @slash_command (name="rgpd", description="Informations sur les RGPD")
    async def rgpd(self, ctx: discord.ApplicationContext):
        plongeur = Plongeur(ctx.user)
        await ctx.respond(content=messages.RGPD, view=MenuInfosStockees(plongeur, self.bot), ephemeral=True)


    @slash_command (name = "recherche_binome", description = "Permet de rechercher un binome")
    async def recherche_binome(self, ctx: discord.ApplicationContext):
        view = MenuRecherche(ctx.bot)

        await ctx.respond(content=messages.RECHERCHE_BINOME, view=view, ephemeral=True)
        return



def setup(bot: ArgoBot):
    bot.add_cog(GeneralCommands(bot))