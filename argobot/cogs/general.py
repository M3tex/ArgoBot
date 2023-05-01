import discord
from menus.recherche_binome import MenuRecherche
import constants.messages as messages
from bot_class import ArgoBot

from discord.ext.commands import Cog, slash_command




class GeneralCommands(Cog):
    
    def __init__(self, bot: ArgoBot):
        super().__init__()
        self.bot = bot
    

    @slash_command (name="rgpd", description="Informations sur les RGPD")
    async def rgpd(self, ctx: discord.ApplicationContext):
        await ctx.respond(content=messages.RGPD, ephemeral=True)


    @slash_command (name = "recherche_binome", description = "Permet de rechercher un binome")
    async def recherche_binome(self, ctx: discord.ApplicationContext):
        view = MenuRecherche(ctx.bot)

        await ctx.respond(content= messages.RECHERCHE_BINOME, view = view, ephemeral = True)
        return




def setup(bot: ArgoBot):
    bot.add_cog(GeneralCommands(bot))