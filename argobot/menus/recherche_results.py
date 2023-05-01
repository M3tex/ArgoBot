import discord
import discord.ext.pages as pages
from plongeur import Plongeur
from constants.embeds import EmbedPlongeur
import constants.messages as messages
import asyncio





class ResultPage(pages.Page):
    embeds: list[EmbedPlongeur]

    def __init__(self, nb_plongeurs: int, embed: EmbedPlongeur):
        self.msg = messages.RECHERCHE_RESULTS.format(nb = nb_plongeurs)
        self.id_plongeur = embed.idPlongeur
        self.nom_plongeur = embed.title

        super().__init__(
            content=self.msg,
            embeds=[embed]
        )


    async def build(self):
        await self.embeds[0].build()
        self.nom_plongeur = self.embeds[0].title


    async def callback(self, interaction: discord.Interaction):
        try:
            await interaction.response.edit_message(content=self.msg)
        except:
            pass




class SearchResults(pages.Paginator):
    pages: list[ResultPage]
    def __init__(self, result: list[EmbedPlongeur]):
        b = [PrevButton(), ContactButton(), NextButton(), IndicButton()]
        
        tmp = len(result)
        pages = [ResultPage(tmp, embed) for embed in result]

        super().__init__(
            pages=pages,
            author_check=True,
            use_default_buttons=False,
            custom_buttons=b,
            trigger_on_display=True
        )




class PrevButton(pages.PaginatorButton):
    def __init__(self):
        super().__init__(
            button_type="prev",
            label="Plongeur précédent",
            emoji="◀️",
            style=discord.ButtonStyle.blurple
        )
    



class ContactButton(pages.PaginatorButton):
    paginator: SearchResults
    def __init__(self):
        
        super().__init__(
            button_type="contact", 
            label="Contacter",
            emoji="📬",
            style=discord.ButtonStyle.green
        )

    async def callback(self, interaction: discord.Interaction):
        current_id = self.paginator.pages[self.paginator.current_page].id_plongeur
        current_name = self.paginator.pages[self.paginator.current_page].nom_plongeur

        msg = messages.RECHERCHE_CONTACT.format(name = current_name, id = current_id)
        
        await interaction.response.edit_message(content=msg)



class NextButton(pages.PaginatorButton):
    paginator: SearchResults

    def __init__(self):
        super().__init__(
            button_type="next",
            label="Plongeur suivant",
            emoji="▶️",
            style=discord.ButtonStyle.blurple
        )
    
    async def callback(self, interaction: discord.Interaction):
        if self.paginator.current_page < self.paginator.page_count:
            self.paginator.current_page += 1

            await self.paginator.pages[self.paginator.current_page].build()
            await self.paginator.goto_page(page_number=self.paginator.current_page, interaction=interaction)





class IndicButton(pages.PaginatorButton):
    def __init__(self):
        super().__init__(
            button_type="page_indicator",
            style=discord.ButtonStyle.gray,
            disabled=True
        )