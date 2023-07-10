import discord
import discord.ext.pages as pages
from globals import CONSTANTES




class ResultPage(pages.Page):
    embeds: list[discord.Embed]

    def __init__(self, nb_plongeurs: int, embed: discord.Embed):
        self.msg = CONSTANTES.messages.RECHERCHE_RESULTS.format(nb = nb_plongeurs)
        self.idPlongeur = int(embed.footer.text.split(': ')[1])
        self.nomPlongeur = embed.title

        super().__init__(
            content=self.msg,
            embeds=[embed]
        )


    async def callback(self, interaction: discord.Interaction):
        try:
            await interaction.response.edit_message(content=self.msg)
        except:
            pass




class SearchResults(pages.Paginator):
    pages: list[ResultPage]
    def __init__(self, result: list[discord.Embed]):
        buttons = [PrevButton(), ContactButton(), NextButton(), IndicButton()]
        
        tmp = len(result)
        pages = [ResultPage(tmp, embed) for embed in result]

        super().__init__(
            pages=pages,
            author_check=True,
            use_default_buttons=False,
            custom_buttons=buttons,
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
        current_id = self.paginator.pages[self.paginator.current_page].idPlongeur
        current_name = self.paginator.pages[self.paginator.current_page].nomPlongeur

        msg = CONSTANTES.messages.RECHERCHE_CONTACT.format(name = current_name, id = current_id)

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
    
    # async def callback(self, interaction: discord.Interaction):
    #     if self.paginator.current_page < self.paginator.page_count:
    #         self.paginator.current_page += 1

    #         await self.paginator.pages[self.paginator.current_page]
    #         await self.paginator.goto_page(page_number=self.paginator.current_page, interaction=interaction)





class IndicButton(pages.PaginatorButton):
    def __init__(self):
        super().__init__(
            button_type="page_indicator",
            style=discord.ButtonStyle.gray,
            disabled=True
        )