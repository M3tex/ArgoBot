import discord
from plongeur import Plongeur
from bot_class import ArgoBot

from globals import global_data, CONSTANTES
import io


# TODO: A refaire entièrement avec Paginator + intégration
# avec les nouvelles classes.


############### Menus à choix multiples (View Subclass) ###############
#                                                                     #
# Documentation `discord.ui.View`:                                    #
# https://docs.pycord.dev/en/stable/api/ui_kit.html#discord.ui.View   #
#                                                                     #
#######################################################################

### Premier Menu à Choix Multiples
class MenuCM1(discord.ui.View):
    def __init__(self, plongeur: Plongeur):
        # Pour récupérer les choix. TODO: Voir si on peut faire mieux
        self.plongeur = plongeur

        listItems = [FederationSelect(), NombrePlongeeSelect(), SpecialitesSelect(),
                      StopButton(), ResetButton(menu = 1), SuivantButton(menu = 1)]
        

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
        listItems = [PratiqueSelect(), InteretSelect(), SearchConsentSelect(), StopButton(), ResetButton(menu = 2), SuivantButton(menu = 2)]
        super().__init__()

        for it in listItems:
            self.add_item(it)
        
        self.plongeur = plongeur


# ! Rien à faire ici, faire un nouveau fichier spécial pour les petits menus

### Information sur collecte de donnée
class MenuInfoCollect(discord.ui.View):
    def __init__(self, plongeur: Plongeur):
        super().__init__()
        self.plongeur = plongeur
        self.add_item(StopButton())
        self.add_item(SuivantButton(menu = 3))


### Données stockées sur utilisateur:
class MenuInfosStockees(discord.ui.View):
    def __init__(self, plongeur: Plongeur, bot: ArgoBot):
        super().__init__()
        self.add_item(GetInfoButton(plongeur, bot))


### Affichage infos plongeur RGPD
class MenuAffichageInfos(discord.ui.View):
    def __init__(self, plongeur: Plongeur, msg: str):
        super().__init__()
        self.msg = msg
        self.add_item(StopButton())
        self.add_item(DeleteInfoButton(plongeur))
        self.add_item(DLInfoButton(plongeur))


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
        super().__init__(title = "Dernières questions")
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
            content = CONSTANTES.messages.CREATION_SUCCESS,
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
    view: MenuCM1
    def __init__(self):
        super().__init__(
            placeholder = "Fédération",
            min_values = 1,
            max_values = len(CONSTANTES.select_options.FEDERATIONS),
            row = 0,
            options = CONSTANTES.select_options.FEDERATIONS,
        )
    
    # Override de la méthode callback (appelée après une intéraction)
    async def callback(self, interaction: discord.Interaction):
        fede_selected = [int(x) for x in self.values]
        opt_niveaux = []

        for fede in fede_selected:
            # Pour ne proposer que les niveaux des fédérations sélectionnées
            for niv in global_data.niveaux:
                if fede in niv.federations and niv.select_option not in opt_niveaux:
                    opt_niveaux.append(niv.select_option)
        
        self.view.plongeur.federations = [global_data.get_info("Federation", id) 
                                          for id in fede_selected]
        self.view.add_item(NiveauSelect(opt_niveaux))
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

  
    async def callback(self, interaction: discord.Interaction):
        self.view.plongeur.niveaux = [global_data.get_info("Niveau", int(id)) 
                                      for id in self.values]
        await interaction.response.defer()


### Choix du nombre de plongées max
class NombrePlongeeSelect(discord.ui.Select):
    def __init__(self):
        super().__init__(
            placeholder = "Nombre de plongées",
            min_values = 1,
            max_values = 1,
            row = 2,
            options = CONSTANTES.select_options.NOMBRE_PLONGEES
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
            max_values = len(CONSTANTES.select_options.SPECIALITES),
            options = CONSTANTES.select_options.SPECIALITES
        )
    
    async def callback(self, interaction: discord.Interaction):
        self.view.plongeur.specialites = [global_data.get_info("Specialite", int(id)) 
                                          for id in self.values]
        await interaction.response.defer()



### Choix de la pratique
class PratiqueSelect(discord.ui.Select):
    def __init__(self):
        super().__init__(
        placeholder = "Pratique",
        min_values = 1,
        max_values = 2,
        row = 0,
        options = CONSTANTES.select_options.PRATIQUE
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
        max_values = len(CONSTANTES.select_options.INTERETS),
        row = 2,
        options = CONSTANTES.select_options.INTERETS
    )
    
    async def callback(self, interaction: discord.Interaction):
        self.view.plongeur.interets = [global_data.get_info("Interet", int(id)) 
                                      for id in self.values]
        await interaction.response.defer()



### Professions
class ProfessionSelect(discord.ui.Select):
    def __init__(self):
        super().__init__(
            placeholder = "Profession",
            min_values = 1,
            max_values = len(CONSTANTES.select_options.PROFESSIONS),
            row = 1,
            options = CONSTANTES.select_options.PROFESSIONS,
            custom_id = "professions"
        )

    async def callback(self, interaction: discord.Interaction):
        self.view.plongeur.profession = [global_data.get_info("Profession", int(id)) 
                                        for id in self.values]
        await interaction.response.defer()
    


### Être affiché dans les résultats de recherche de binôme:
class SearchConsentSelect(discord.ui.Select):
    def __init__(self):
        super().__init__(
            placeholder="Apparaître dans les résultats de recherche ?",
            min_values=1,
            max_values=1,
            row=3,
            options= CONSTANTES.select_options.CHOIX_REFERENCEMENT
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
            options = CONSTANTES.select_options.HELP_PLONGEURID
        )

    async def callback(self, interaction: discord.Interaction):
        cmd_to_help = {
            "création": CONSTANTES.messages.HELP_CREATION,
            "suppression": CONSTANTES.messages.HELP_SUPPRESSION,
            "carte": CONSTANTES.messages.HELP_CARTE
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
                content = CONSTANTES.messages.CREATION_INCOMPLET + CONSTANTES.messages.CREATION_MENU_1
            )
        else:
            await interaction.response.edit_message (
                content = CONSTANTES.messages.CREATION_MENU_2,
                view=MenuCM2(self.view.plongeur)
            )


    async def __callback_menu2(self, interaction: discord.Interaction):
        plongeur: Plongeur = self.view.plongeur

        # TODO: Rendre le champs activité pro obligatoire ???
        if not plongeur.menu2_est_complet():
            await self.view.get_item("rst_button").callback_menu2 (
                interaction,
                content = CONSTANTES.messages.CREATION_INCOMPLET + CONSTANTES.messages.CREATION_MENU_2
            )
        else:
            await interaction.response.send_modal(MenuText(self.view.plongeur))
    

    # On override la fonction appelée et on appelle le bon callback
    async def callback(self, interaction: discord.Interaction):
        if self.menu == 1:
            await self.__callback_menu1(interaction)
        elif self.menu == 2:
            await self.__callback_menu2(interaction)
        elif self.menu == 3:
            msg = CONSTANTES.messages.CREATION_MENU_1
            await interaction.response.edit_message(content=msg, view=MenuCM1(self.view.plongeur))
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
    async def callback_menu1(self, interaction: discord.Interaction, content=CONSTANTES.messages.CREATION_MENU_1):
        self.view.enable_all_items()
        tmp = self.view.get_item("niveaux")
        if tmp:
            self.view.remove_item(tmp)
        self.view.plongeur.reset_menu1()
        await interaction.response.edit_message(content = content, view=self.view)


    async def callback_menu2(self, interaction: discord.Interaction, content=CONSTANTES.messages.CREATION_MENU_1):
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
            content = CONSTANTES.messages.ABANDON_CREATION,
            view=self.view, embed=None
        )


class GetInfoButton(discord.ui.Button):
    def __init__(self, plongeur: Plongeur, bot: ArgoBot):
        super().__init__(
            label="Mes informations",
            style=discord.ButtonStyle.blurple,
            row = 4
        )
        self.plongeur = plongeur
        self.bot = bot
    
    
    async def callback(self, interaction: discord.Interaction):
        if await self.plongeur.est_dans_db():
            rep = await self.plongeur.to_embed()
            msg = f"## Voici vos informations:\n\n"
            msg += f"Identifiant Discord: `{self.plongeur.user.id}`\n"
            msg += f"Consent à apparaître dans les résultats de recherche de binome: "
            msg += "`oui`" if self.plongeur.search_consent else "`non`"
            await interaction.response.edit_message(content=msg, embed=rep, view=MenuAffichageInfos(self.plongeur, msg))
        else:
            await interaction.response.edit_message(content=CONSTANTES.messages.PLONGEUR_INEXISTANT, view=None)


class DeleteInfoButton(discord.ui.Button):
    def __init__(self, plongeur: Plongeur):
        super().__init__(
            label="Supprimer mes informations",
            style=discord.ButtonStyle.blurple,
            row=4
        )
        self.plongeur = plongeur
    

    async def callback(self, interaction: discord.Interaction):
        await self.plongeur.supprime()

        msg = CONSTANTES.messages.SUPPRESSION_PLONGEUR.format(interaction.user.display_name)
        await interaction.response.edit_message(content=msg, view=None, embed=None)


class DLInfoButton(discord.ui.Button):
    view: MenuAffichageInfos
    def __init__(self, plongeur: Plongeur):
        super().__init__(
            label="Télécharger mes données",
            style=discord.ButtonStyle.green,
            row=4
        )
        self.plongeur = plongeur
        self.fichier_envoye = False
    

    async def callback(self, interaction: discord.Interaction):
        if not self.fichier_envoye:
            with io.StringIO() as fp:
                fp.write(await self.plongeur.to_json())
                fp.seek(0)
                f = discord.File(fp=fp, filename=f"{self.plongeur.prenom}.json")

            msg = "## Voici vos données au format `JSON`"
            self.label = "Afficher mes données"
            await interaction.response.edit_message(content=msg, embed=None, file=f, view=self.view)
        else:
            self.label = "Télécharger mes données"
            emb = await self.plongeur.to_embed()
            await interaction.response.edit_message(content=self.view.msg, attachments=[], embed=emb, view=self.view)

        self.fichier_envoye = not self.fichier_envoye
        

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


