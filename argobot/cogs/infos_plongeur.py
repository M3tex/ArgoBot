import discord
from plongeur import Plongeur
import menus.creation_infos_plongeur as menus
from bot_class import ArgoBot
from globals import CONSTANTES
from discord.ext.commands import Cog
from diver_card import create_diver_card


# CoG -> Command Groups
# ? Doc: https://guide.pycord.dev/popular-topics/cogs


# Ce fichier contient les commandes contenues dans le groupe `infos_plongeur`
#
# Actuellement:
# /infos_plongeur aide
# /infos_plongeur carte
# /infos_plongeur création
# /infos_plongeur suppression



class InfosPlongeur(Cog):
    group = discord.SlashCommandGroup(
        name = "infos_plongeur",
        description = "Toutes les commandes liées aux infos de plongeur !"
    )
    

    def __init__(self, bot: ArgoBot):
        self.bot = bot



    @group.command (
        name="aide",
        description="Affiche une description détaillée de toutes les commandes"
    )
    async def aide(self, ctx: discord.ApplicationContext):
        await ctx.respond(CONSTANTES.messages.HELP_PLONGEURID, view=menus.MenuHelp(), ephemeral=True)
        return



    @group.command (
        name="création",
        description="Permet de saisir tes informations de plongeur !"
    )
    async def creation(self, ctx: discord.ApplicationContext):
        if self.bot.is_infos_plongeur_locked():
            await ctx.respond(CONSTANTES.messages.INFO_CREA_LOCKED, ephemeral = True)
            return

        plongeur = Plongeur(ctx.author)
        view = menus.MenuCM1(plongeur)
        
        if await plongeur.est_dans_db():
            await ctx.respond(CONSTANTES.messages.CREATION_MENU_1, view=view, ephemeral=True)
        else:
            await ctx.respond(CONSTANTES.messages.WARNING_RGPD, view=menus.MenuInfoCollect(plongeur), ephemeral = True)
        return



    # ? Enlever le param optionnel sur la commande publique et faire une commande admin dédiée ?
    @group.command (
        name = "suppression",
        description = "Permet de supprimer tes informations de la base de données"
    )
    @discord.option(
        name="user",
        type=discord.Member,
        required=False,
        default=None,
        description="Administrateurs seulement. L'utilisateur à supprimer."
    )
    async def suppression(self, ctx: discord.ApplicationContext, user: discord.Member):

        if self.bot.is_infos_plongeur_locked():
            await ctx.respond(CONSTANTES.messages.INFO_CREA_LOCKED, ephemeral = True)
            return

        to_remove = ctx.author

        if user != None:
            to_remove = user
            if (not ctx.author.guild_permissions.administrator) and user != ctx.author:
                await ctx.respond("Vous n'avez pas la permission de supprimer un autre membre de la base de données.", ephemeral=True)
                return

        await Plongeur(to_remove).supprime()
        
        await ctx.respond(CONSTANTES.messages.SUPPRESSION_PLONGEUR.format(to_remove.display_name), ephemeral=True)
    


    @group.command (
        name = "carte",
        description = "Permet d'afficher ta carte de plongeur !"
    )
    async def carte(self, ctx: discord.ApplicationContext):
        if self.bot.is_cards_locked():
            await ctx.respond(CONSTANTES.messages.INFO_CARD_LOCKED, ephemeral = True)
            return
        
        plongeur = await Plongeur(ctx.author).load_from_db()
        if plongeur == None:
            await ctx.respond(CONSTANTES.messages.PLONGEUR_INEXISTANT, ephemeral = True)
            return
 
        carte = await plongeur.get_card()
        await ctx.respond(file=carte, ephemeral=True)
      



def setup(bot: ArgoBot):
    cog = InfosPlongeur(bot)

    bot.add_cog(cog)
