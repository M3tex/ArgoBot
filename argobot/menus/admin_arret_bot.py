import discord
from bot_class import ArgoBot


class MenuArretBot(discord.ui.View):
    def __init__(self, bot: ArgoBot):
        self.bot = bot
        items = [AnnulationButton(), ConfirmationButton()]
        super().__init__()

        for it in items:
            self.add_item(it)




class AnnulationButton(discord.ui.Button):
    view: MenuArretBot
    def __init__(self):
        super().__init__(
            label = "Revenir en arrière",
            style = discord.ButtonStyle.gray,
            row = 0
        )
    

    async def callback(self, interaction: discord.Interaction):
        self.view.disable_all_items()
        await interaction.response.edit_message(view=self.view, content="*Arrêt annulé :x:*")




class ConfirmationButton(discord.ui.Button):
    view: MenuArretBot
    def __init__(self):
        super().__init__(
            label = "ARRÊTER LE BOT",
            style = discord.ButtonStyle.danger,
            row = 0
        )
    

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.edit_message(view=None, content="*Le bot est hors-ligne*")
        await self.view.bot.arret(interaction.user)

