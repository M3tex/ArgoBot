import discord
from bot_class import ArgoBot
import constants.messages as messages
import constants.sql_request as requests
from discord.ext.pages import Paginator, Page
from database import connexion
from constants.embeds import EmbedStatPlongeur



# Menu d'administration pour les commandes liées aux infos de plongeur

class MenuAdminInfosPlongeur(discord.ui.View):
    def __init__(self, bot: ArgoBot):
        self.bot = bot

        list_items = [DebloqueCarte(), BloqueCarte(), DebloqueDonnees(), BloqueDonnees(), StatsPlongeur()]
        super().__init__()

        for it in list_items:
            self.add_item(it)
        
        self.update()

    
    # ? voir si on fait autrement
    def update(self):
        bdd_locked = self.bot.is_infos_plongeur_locked()
        self.get_item("lock_db").disabled = bdd_locked
        self.get_item("unlock_db").disabled = not bdd_locked

        card_locked = self.bot.is_cards_locked()
        self.get_item("lock_cards").disabled = card_locked
        self.get_item("unlock_cards").disabled = not card_locked




class DebloqueCarte(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label = "Débloquer les cartes",
            style = discord.ButtonStyle.success,
            row = 0,
            emoji="🔓",
            custom_id="unlock_cards"
        )
    

    async def callback(self, interaction: discord.Interaction):
        self.view.bot.unlock_cards()
        self.view.update()
        await interaction.response.edit_message(view=self.view, content=messages.ADMIN_UNLOCKED_CARDS)



class BloqueCarte(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label = "Bloquer les cartes",
            style = discord.ButtonStyle.danger,
            row = 0,
            emoji="🔒",
            custom_id="lock_cards"
        )
    

    async def callback(self, interaction: discord.Interaction):
        self.view.bot.lock_cards()
        self.view.update()
        await interaction.response.edit_message(view=self.view, content=messages.ADMIN_LOCKED_CARDS)



class DebloqueDonnees(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label = "Débloquer les données",
            style = discord.ButtonStyle.success,
            row = 1,
            emoji="🔓",
            custom_id="unlock_db"
        )
    

    async def callback(self, interaction: discord.Interaction):
        self.view.bot.unlock_infos_plongeur()
        self.view.update()
        await interaction.response.edit_message(view=self.view, content=messages.ADMIN_UNLOCKED_DB)



class BloqueDonnees(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label = "Bloquer les données",
            style = discord.ButtonStyle.danger,
            row = 1,
            emoji="🔒",
            custom_id="lock_db"
        )
    

    async def callback(self, interaction: discord.Interaction):
        self.view.bot.lock_infos_plongeur()
        self.view.update()
        await interaction.response.edit_message(view=self.view, content=messages.ADMIN_LOCKED_DB)



class StatsPlongeur(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label="Statistiques",
            style = discord.ButtonStyle.primary,
            emoji="📊",
            row = 2
        )

    
    async def callback(self, interaction: discord.Interaction):
        embed = EmbedStatPlongeur()
        await embed.set_stats()
        await interaction.response.edit_message(view = None, embed = embed)
