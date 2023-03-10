import discord
from discord.ext.commands import Cog
from bot_class import ArgoBot
import constants.messages as messages
from menus.admin_infos_plongeur import Menu



# Commandes d'administration

class Admin(Cog):
    admin_group = discord.SlashCommandGroup(
        name = "admin",
        description="Les commandes d'administration",
        default_member_permissions = discord.Permissions(administrator=True)
    )

    def __init__(self, bot: ArgoBot):
        self.bot = bot

    

    #------------- Dashboard infos plongeur -------------#

    @admin_group.command(
        name="infos_plongeur",
        description="Administrateurs seulement. Permet de gérer les systèmes `infos_plongeur`"
    )
    @discord.default_permissions(administrator=True,)
    async def infos_plongeur(self, ctx: discord.ApplicationContext):
        if not ctx.author.guild_permissions.administrator:
            await ctx.respond(messages.NOT_ADMIN, ephemeral=True)
            return

        await ctx.respond(view=Menu(self.bot), ephemeral=True)
    

    
    #------------- Dashboard recherche binome -------------#




def setup(bot: ArgoBot):
    cog = Admin(bot)

    bot.add_cog(cog)