import discord
import database
from menus.recherche_results import SearchResults
from bot_class import ArgoBot
from plongeur import Plongeur
from globals import CONSTANTES



default_request = "SELECT idPlongeur FROM Plongeur WHERE consent = 1 AND idPlongeur IN ("


class MenuRecherche(discord.ui.View):
    criteres = ["Federation", "Niveau", "Specialite", "Interet"]
    no_page = 0
    request = default_request
    last_request = ""

    def __init__(self, bot: ArgoBot):
        self.result = []        # Contiendra les idPlongeurs du résultat
        self.operator = ""      # L'opérateur logique choisit (AND ou OR)
        self.federations = []
        self.niveaux = []
        self.specialites = []
        self.interets = []

        self.bot = bot
        

        self.crit2list = {
            "Federation": self.federations,
            "Niveau": self.niveaux,
            "Specialite": self.specialites,
            "Interet": self.interets
        }


        super().__init__()

        self.add_item(CritereSelect("Federation"))
        self.add_item(OperatorSelect())
        
        tmp = f"{self.no_page + 1}/{len(self.criteres)}"

        buttons = [PrecedentButton(), CancelButton(), SuivantButton("Federation"), PageCounter(tmp)]
        for b in buttons:
            self.add_item(b)

        
    

    def update(self):
        # On supprime les anciens items
        self.clear_items()
        self.operator = ""

        # On rajoute le critère actuel
        self.add_item(CritereSelect(self.criteres[self.no_page]))
        self.add_item(OperatorSelect())

        tmp = f"{self.no_page + 1}/{len(self.criteres)}"

        # Les boutons
        self.add_item(PrecedentButton())
        self.add_item(CancelButton()),
        self.add_item(SuivantButton(self.criteres[self.no_page]))
        self.add_item(PageCounter(tmp))

        
        



class OperatorSelect(discord.ui.Select):
    view: MenuRecherche

    def __init__(self):
        super().__init__(
            placeholder="Opérateur",
            min_values=1,
            max_values=1,
            options=CONSTANTES.select_options.OPERATEURS
        )
    

    async def callback(self, interaction: discord.Interaction):
        self.view.operator = self.values[0]
        await interaction.response.defer()




class CritereSelect(discord.ui.Select):
    view: MenuRecherche

    def __init__(self, critere: str):
        # On récupère les options dépendantes du critère
        critere_aucun = CONSTANTES.select_options.AUCUN_CRITERE
        CRITERE2OPTIONS = {
            "Federation": [critere_aucun] + CONSTANTES.select_options.FEDERATIONS.copy(),
            "Niveau": [critere_aucun] + CONSTANTES.select_options.NIVEAUX.copy(),
            "Specialite": [critere_aucun] + CONSTANTES.select_options.SPECIALITES.copy(),
            "Interet": [critere_aucun] + CONSTANTES.select_options.INTERETS.copy()
        }

        opt = CRITERE2OPTIONS.get(critere, None)
        if opt == None:
            print("Erreur de clé lors de la création du menu de sélection de critère")
            print(f"Clé: {critere}")
            return


        # Purement visuel, pour les accents etc.
        key2label = {
            "Federation": "Fédérations",
            "Niveau": "Niveaux",
            "Specialite": "Spécialités",
            "Interet": "Intérêts"
        }


        super().__init__(
            placeholder=key2label[critere],
            min_values=1,
            max_values=len(opt),
            options=opt
        )

        self.critere = critere

    
    async def callback(self, interaction: discord.Interaction):
        self.view.crit2list[self.critere] = None if "Aucun" in self.values else [int(val) for val in self.values]

        await interaction.response.defer()




class PrecedentButton(discord.ui.Button):
    view: MenuRecherche

    def __init__(self):
        super().__init__(
            label="Critère précédent",
            style=discord.ButtonStyle.gray,
            row=4,
            custom_id="prec_button"
        )
    

    async def callback(self, interaction: discord.Interaction):
        if self.view.no_page >= 1:
            # On supprime la sous-requête précedente
            self.view.request = self.view.request.removesuffix(self.view.last_request)
            self.view.no_page -= 1
            self.view.update()
        
        await interaction.response.edit_message(view=self.view)



class CancelButton(discord.ui.Button):
    view: MenuRecherche

    def __init__(self):
        super().__init__(
            label="Annuler la recherche",
            style=discord.ButtonStyle.danger,
            row=4,
            custom_id="cncl_button"
        )
    

    async def callback(self, interaction: discord.Interaction):
        self.view.disable_all_items()
        self.view.stop()
        await interaction.response.edit_message(content="Recherche annulée", view=self.view)




class SuivantButton(discord.ui.Button):
    view: MenuRecherche

    def __init__(self, critere: str):
        super().__init__(
            label="Critère suivant",
            style=discord.ButtonStyle.primary,
            row=4,
            custom_id="suiv_button"
        )

        self.critere = critere
    

    async def callback(self, interaction: discord.Interaction):
        # On génère la requête SQL permettant d'obtenir l'ensemble des 
        # plongeurs matchant avec le critère
        table = "PlongeurPossede" + self.critere
        request = f"SELECT idPlongeur FROM {table} "
        op = "WHERE"    # Pour le premier

        values = self.view.crit2list[self.critere]
        guild = interaction.guild
        bot = interaction.client
        msg = interaction.message

        # todo: voir si moyen simple de faire des requêtes moins longues

        # si "Aucun" est sélectionné (i.e le critère n'est pas pertinent) alors
        # rien à faire on passe à la page suivante
        if values != None:
            # On vérifie que tout ait été saisit.
            # Si un seul critère choisit, pas besoin d'opérateur
            if not values or (not self.view.operator and len(values) != 1):
                await interaction.response.edit_message(content=CONSTANTES.messages.CREATION_INCOMPLET, view=self.view)
                return
        
            for id in values:
                # On se permet de formater les valeurs directement car rien de ce qui est formatté
                # n'est modifiable / saisit par les utilisateurs
                request += f"{op} idPlongeur IN "
                request += f"(SELECT idPlongeur FROM {table} WHERE id{self.critere} = {id}) "

                op = self.view.operator
        
        
            # On ajoute la sous requête
            self.view.last_request = f" INTERSECT {request}" if self.view.no_page > 0 and self.view.request != default_request else f"{request}"
            self.view.request += self.view.last_request


        if self.view.no_page + 1 < len(self.view.criteres):
            self.view.no_page += 1
            self.view.update()
        
            await interaction.response.edit_message(view=self.view)
            return
        
        else:
            await interaction.response.defer(ephemeral=True, invisible=False)

            # Pas réussi à modifier le message original avec l'embed
            await interaction.followup.delete_message(interaction.message.id)

            conn = await database.connexion()
            cur = await conn.cursor()
            
            # Si aucun critère n'a été pertinent (= on cherche tous les plongeurs)
            if self.view.request == default_request:
                self.view.request = "SELECT idPlongeur FROM Plongeur WHERE consent = 1;"
            else:
                self.view.request += ');'
            
            try:
                results = await (await cur.execute(self.view.request)).fetchall()
            except:
                print(f"Erreur requête:")
                print(self.view.request)
                await self.view.disable_all_items()

                # <@461249475999170582> -> mon id discord
                await interaction.followup.send(content="Une erreur a eu lieu, contactez <@461249475999170582>")

            await cur.close()
            await conn.close()


            pages = []
            for id in results:
                plongeur = guild.get_member(id[0])
                
                # Principalement pour tester sur le serv de test
                # car tous les plongeurs de la db ne sont pas dans le serveur
                # de test.
                if not plongeur:
                    plongeur = await bot.get_or_fetch_user(id[0])
                    if not plongeur: continue
                
                pages.append(await Plongeur(plongeur).to_embed())
            
            if pages:
                test = SearchResults(pages)
                # await test.edit(message=msg)      # Ne fonctionne pas
                await test.respond(interaction, ephemeral=True)
            else:
                await interaction.followup.send(content="Aucun plongeur ne correspond à vos critères", ephemeral=True)



class PageCounter(discord.ui.Button):
    view: MenuRecherche

    def __init__(self, nb_pages: str):
        super().__init__(
            label=nb_pages,
            style=discord.ButtonStyle.gray,
            row=4,
            custom_id="page_button",
            disabled=True
        )
