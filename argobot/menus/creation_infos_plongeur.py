import discord
import constants.select_options as options
import constants.messages as messages
from plongeur import Plongeur






############### Menus à choix multiples (View Subclass) ###############
#                                                                     #
# Documentation `discord.ui.View`:                                    #
# https://docs.pycord.dev/en/stable/api/ui_kit.html#discord.ui.View   #
#                                                                     #
#######################################################################

### Premier Menu à Choix Multiples
class MenuCM1(discord.ui.View):
    opt_niveaux: list[discord.SelectOption] = []

    def __init__(self, plongeur: Plongeur):
        # Pour récupérer les choix. TODO: Voir si on peut faire mieux
        self.plongeur = plongeur

        listItems = [FederationSelect(), NombrePlongeeSelect(), SpecialitesSelect(),
                     SuivantButton(menu = 1), ResetButton(menu = 1), StopButton()]
        

        super().__init__()
        for it in listItems:
            self.add_item(it)




    # Réinitialise le menu. Appelée quand le bouton 'Réinitialiser' est cliqué
    def reset(self):
        # Pas de nouvelle instance de Plongeur car si menu2 on garde les choix précédents
        # Donc j'ai gardé le même paterne pour reset le menu 1
        self.plongeur.reset_menu1()
        self.__init__(self.plongeur)




### Deuxième Menu à Choix Multiples
class MenuCM2(discord.ui.View):
    
    def __init__(self, plongeur: Plongeur):
        listItems = [PratiqueSelect(), InteretSelect(), SearchConsentSelect(), SuivantButton(menu = 2), ResetButton(menu = 2), StopButton()]
        super().__init__()

        for it in listItems:
            self.add_item(it)
        
        self.plongeur = plongeur



### Menu d'aide
class MenuHelp(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(CmdSelect())



#################### Menu Textuel (Modal Subclass) ####################
#                                                                     #
# Documentation `discord.ui.Modal`:                                   #
# https://docs.pycord.dev/en/stable/api/ui_kit.html#discord.ui.Modal  #
#                                                                     #
#######################################################################

class MenuText(discord.ui.Modal):
    def __init__(self, plongeur: Plongeur):
        super().__init__(title = "Petit Questionnaire")
        listItems = [PseudoInput(), RegionInput(), DescriptionInput()]

        for it in listItems:
            self.add_item(it)

        self.plongeur = plongeur


    async def callback(self, interaction: discord.Interaction):
        self.plongeur.prenom = self.children[0].value
        self.plongeur.region = self.children[1].value
        self.plongeur.description = self.children[2].value


        # Normalement pas d'erreur possible mais:
        # TODO: vérifier l'insertion dans insere_plongeur et traiter les erreurs
        await self.plongeur.to_db()

        return await interaction.response.edit_message (
            content = messages.CREATION_SUCCESS,
            view=None
        )



################## Choix déroulants (Select Subclass) ##################
#                                                                      #
# Documentation `discord.ui.Select`:                                   #
# https://docs.pycord.dev/en/stable/api/ui_kit.html#discord.ui.Select  #
#                                                                      #
########################################################################

### Choix des fédérations
class FederationSelect(discord.ui.Select):

    def __init__(self):
        super().__init__(
            placeholder = "Fédération",
            min_values = 1,
            max_values = len(options.FEDERATIONS),
            row = 0,
            options = options.FEDERATIONS,
            
        )
    
    # Override de la méthode callback (appelée après une intéraction)
    async def callback(self, interaction: discord.Interaction):
        fede_selected = self.values

        # 0 est l'id de la FFESSM. TODO: trouver + lisible ?   
        if "0" in fede_selected:
            self.view.opt_niveaux += [el for el in options.NIVEAUX_FFESSM if el not in self.view.opt_niveaux]
        
        # 1 est l'id de PADI
        if "1" in fede_selected:
            self.view.opt_niveaux += [el for el in options.NIVEAUX_PADI if el not in self.view.opt_niveaux]

        # 2 est l'id de SSI
        if "2" in fede_selected:
            self.view.opt_niveaux += [el for el in options.NIVEAUX_SSI if el not in self.view.opt_niveaux]


        self.view.plongeur.federations = [int(id) for id in fede_selected]
        self.view.add_item(NiveauSelect(self.view.opt_niveaux))
        self.disabled = True
        await interaction.response.edit_message(view=self.view)



### Choix des niveaux (dynamique en fonction des choix de fédés)
class NiveauSelect(discord.ui.Select):
    def __init__(self, options: list[discord.SelectOption]):
        super().__init__(
            placeholder = "Niveau",
            min_values = 1,
            max_values = len(options),
            options = options,
            custom_id = "niveaux",
        )

    # Override de la méthode callback (appelée après une intéraction)    
    async def callback(self, interaction: discord.Interaction):
        self.view.plongeur.niveaux = [int(id) for id in self.values]
        await interaction.response.defer()


### Choix du nombre de plongées max
class NombrePlongeeSelect(discord.ui.Select):
    def __init__(self):
        super().__init__(
            placeholder = "Nombre de plongées",
            min_values = 1,
            max_values = 1,
            row = 2,
            options = options.NOMBRE_PLONGEES
        )
    
    async def callback(self, interaction: discord.Interaction):
        self.view.plongeur.nombre_plongee = int(self.values[0])
        await interaction.response.defer()



### Choix des Spécialités
class SpecialitesSelect(discord.ui.Select):
    def __init__(self):
        super().__init__(
            placeholder = "Spécialités",
            min_values = 1,
            row = 3,
            max_values = len(options.SPECIALITES),
            options = options.SPECIALITES
        )
    
    async def callback(self, interaction: discord.Interaction):
        self.view.plongeur.specialites = [int(id) for id in self.values]
        await interaction.response.defer()



### Choix de la pratique
class PratiqueSelect(discord.ui.Select):
    def __init__(self):
        super().__init__(
        placeholder = "Pratique",
        min_values = 1,
        max_values = 2,
        row = 0,
        options = options.PRATIQUE
    )
    
    async def callback(self, interaction: discord.Interaction):
        # 1 est l'id de Professionel
        if "1" in self.values:
            self.view.add_item(ProfessionSelect())
        
        self.disabled = True
        self.view.plongeur.pratique = [int(id) for id in self.values]
        await interaction.response.edit_message(view=self.view)



### Choix des intérêts
class InteretSelect(discord.ui.Select):
    def __init__(self):
        super().__init__(
        placeholder = "Interêts",
        min_values = 1,
        max_values = len(options.INTERETS),
        row = 2,
        options = options.INTERETS
    )
    
    async def callback(self, interaction: discord.Interaction):
        self.view.plongeur.interets = [int(id) for id in self.values]
        await interaction.response.defer()



### Professions
class ProfessionSelect(discord.ui.Select):
    def __init__(self):
        super().__init__(
            placeholder = "Profession",
            min_values = 1,
            max_values = len(options.PROFESSIONS),
            row = 1,
            options = options.PROFESSIONS,
            custom_id = "professions"
        )

    async def callback(self, interaction: discord.Interaction):
        self.view.plongeur.profession = [int(id) for id in self.values]
        await interaction.response.defer()
    


### Être affiché dans les résultats de recherche de binôme:
class SearchConsentSelect(discord.ui.Select):
    def __init__(self):
        super().__init__(
            placeholder="Rendre mes données publiques ?",
            min_values=1,
            max_values=1,
            row=3,
            options= options.CHOIX_REFERENCEMENT
        )
    
    async def callback(self, interaction: discord.Interaction):
        self.view.plongeur.search_consent = bool(int(self.values[0]))
        await interaction.response.defer()



### Choix de la commande d'aide
class CmdSelect(discord.ui.Select):
    def __init__(self):
        super().__init__(
            placeholder="Commande",
            min_values=1,
            max_values=1,
            options = options.HELP_PLONGEURID
        )

    async def callback(self, interaction: discord.Interaction):
        cmd_to_help = {
            "création": messages.HELP_CREATION,
            "suppression": messages.HELP_SUPPRESSION,
            "carte": messages.HELP_CARTE
        }
        await interaction.response.edit_message(content=cmd_to_help[self.values[0]], view=None)



###################### Boutons (Select Subclass) ######################
#                                                                     #
# Documentation `discord.ui.Button`:                                  #
# https://docs.pycord.dev/en/stable/api/ui_kit.html#discord.ui.Button #
#                                                                     #
#######################################################################

### Bouton suivant
class SuivantButton(discord.ui.Button):
    menu: int

    # menu permet de changer l'action en fonction du menu
    def __init__(self, menu):
        super().__init__(
            label = "Suivant",
            style = discord.ButtonStyle.primary,
            row = 4
        )
        self.menu = menu
    
    # On fait 2 méthodes de callback: 1 pour chaque menu
    async def __callback_menu1(self, interaction: discord.Interaction):
        plongeur: Plongeur = self.view.plongeur

        # On vérifie que tous les champs sont remplis
        if not plongeur.menu1_est_complet():
            # S'ils ne sont pas tous remplis on reset
            # TODO: Trouver une manière + propre que de passer par le callback du reset ?
            await self.view.get_item("rst_button").callback_menu1 (
                interaction,
                content = messages.CREATION_INCOMPLET + messages.MENU_1
            )
        else:
            await interaction.response.edit_message (
                content = messages.MENU_2,
                view=MenuCM2(self.view.plongeur)
            )


    async def __callback_menu2(self, interaction: discord.Interaction):
        plongeur: Plongeur = self.view.plongeur

        # TODO: Rendre le champs activité pro obligatoire ???
        if not plongeur.menu2_est_complet():
            await self.view.get_item("rst_button").callback_menu2 (
                interaction,
                content = messages.CREATION_INCOMPLET + messages.MENU_2
            )
        else:
            await interaction.response.send_modal(MenuText(self.view.plongeur))
    

    # On override la fonction appelée et on appelle le bon callback
    async def callback(self, interaction: discord.Interaction):
        if self.menu == 1:
            await self.__callback_menu1(interaction)
        elif self.menu == 2:
            await self.__callback_menu2(interaction)
        else:   # ne devrait pas arriver mais au cas où
            await interaction.response.defer()



class ResetButton(discord.ui.Button):
    menu: int

    def __init__(self, menu):
        super().__init__(
            label = "Réinitialiser",
            style = discord.ButtonStyle.secondary,
            row = 4,
            custom_id = "rst_button"
        )
        self.menu = menu

    # On fait 2 méthodes de callback: 1 pour chaque menu
    async def callback_menu1(self, interaction: discord.Interaction, content = messages.MENU_1):
        self.view.opt_niveaux = []
        self.view.enable_all_items()
        tmp = self.view.get_item("niveaux")
        if tmp:
            self.view.remove_item(tmp)
        self.view.plongeur.reset_menu1()
        await interaction.response.edit_message(content = content, view=self.view)


    async def callback_menu2(self, interaction: discord.Interaction, content = messages.MENU_1):
        self.view.enable_all_items()
        tmp = self.view.get_item("professions")
        if tmp:
            self.view.remove_item(tmp)
        self.view.plongeur.reset_menu2()
        await interaction.response.edit_message(content = content, view=self.view)
    

    # On override la méthode par défaut et on appelle le bon callback
    async def callback(self, interaction: discord.Interaction):
        if self.menu == 1:
            await self.callback_menu1(interaction)
        elif self.menu == 2:
            await self.callback_menu2(interaction)
        else:   # ne devrait pas arriver mais au cas où
            await interaction.response.defer()



class StopButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label = "Abandonner",
            style = discord.ButtonStyle.danger,
            row = 4
        )

    async def callback(self, interaction: discord.Interaction):
        self.view.disable_all_items()
        self.view.stop()
        await interaction.response.edit_message(
            content = messages.ABANDON_CREATION,
            view=self.view
        )


################## Champs Textuels (InputText Subclass) ##################
#                                                                        #
# Documentation `discord.ui.InputText`:                                  #
# https://docs.pycord.dev/en/stable/api/ui_kit.html#discord.ui.InputText #
#                                                                        #
##########################################################################
class PseudoInput(discord.ui.InputText):
    def __init__(self):
        super().__init__(
            label = "Prénom ou Pseudo",
            style = discord.InputTextStyle.singleline,
            placeholder = "Exemple: Argonaute",
            max_length = 50,
            row = 0
        )
        


class RegionInput(discord.ui.InputText):
    def __init__(self):
        super().__init__(
            label = "Région", 
            style = discord.InputTextStyle.singleline,
            placeholder = "La région où vous résidez (ou le pays si à l'étranger)",
            max_length = 50,
            row = 1
        )



class DescriptionInput(discord.ui.InputText):
    def __init__(self):
        super().__init__(
            label="Petite description", 
            style=discord.InputTextStyle.long,
            placeholder="Une description (optionnelle) si vous souhaitez préciser quelques points.",
            required=False,
            row = 2
        )


