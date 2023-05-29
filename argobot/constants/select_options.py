import discord


# ---------- Menu création plongeur ---------- #

# Initialisés dans globals.py
FEDERATIONS: list[discord.SelectOption] = [None]
NIVEAUX: list[discord.SelectOption] = [None]
SPECIALITES: list[discord.SelectOption] = [None]
INTERETS: list[discord.SelectOption] = [None]
PROFESSIONS: list[discord.SelectOption] = [None]

# Pratique de la plongée (loisir ou pro)
PRATIQUE: list[discord.SelectOption] = [
    discord.SelectOption (
        label = "Loisir",
        description = "Je pratique la plongée en loisir",
        emoji = "🏝️",
        value = "0"
    ),
    discord.SelectOption (
        label = "Professionel",
        description = "Je pratique la plongée dans le cadre de mon activité professionnelle",
        emoji = "💵",
        value = "1"
    )
]


# Consentement apparition résultats recherche binome
CHOIX_REFERENCEMENT: list[discord.Option] = [
    discord.SelectOption (
        label = "Oui",
        description = "Je souhaite apparaître dans les résultats de recherche de binômes",
        value = "1"
    ),
    discord.SelectOption (
        label = "Non",
        description = "Je ne souhaite pas apparaître dans les résultats de recherche de binômes",
        value = "0"
    )
]




# Nombre de plongées (avec correspondance animal pour les cartes)
__range_nb_plonges = [10, 20, 50, 100, 200, 300, 500, 1000, 2000]
__emoji_corresp = ["<:crevette:1073737219019378718>", "<:meduse:1073737211322847313>",
                   "<:homard:1073737215848501248>", "<:tortue:1073737202007294002>",
                   "<:poisson_clown:1088490620047331348>", "<:phoque:1073737206956556328>",
                   "<:dauphin:1088490925124223076>", "<:requin:1073737803881513010>",
                   "<:orque:1073737194461733035>"]


NOMBRE_PLONGEES: list[discord.SelectOption] = [
    discord.SelectOption (
        label = f"Moins de {val} plongées",
        emoji = emoji,
        value = str(val)
    )
    for val, emoji in zip(__range_nb_plonges, __emoji_corresp)
]




# ---------- Commande aide plongeur ---------- #

HELP_PLONGEURID: list[discord.SelectOption] = [
    discord.SelectOption (
        label = "création",
        description = "Affiche l'aide pour la commande création"
    ),
    discord.SelectOption (
        label = "suppression",
        description = "Affiche l'aide pour la commande suppression"
    ),
    discord.SelectOption (
        label = "carte",
        description = "Affiche l'aide pour la commande carte"
    )
]



# ---------- Menu recherche binôme ---------- #

AUCUN_CRITERE = discord.SelectOption(
    label="Pas de filtre",
    description="Ce critère n'est pas pertinent dans ma recherche",
    value="Aucun"
)

# CRITERE2OPTIONS = {
#     "Federation": [AUCUN_CRITERE] + FEDERATIONS.copy(),
#     "Niveau": [AUCUN_CRITERE] + NIVEAUX.copy(),
#     "Specialite": [AUCUN_CRITERE] + SPECIALITES.copy(),
#     "Interet": [AUCUN_CRITERE] + INTERETS.copy()
# }


OPERATEURS: list[discord.SelectOption] = [
    discord.SelectOption(
        label="ET",
        description="Les plongeurs ayant TOUS les critères sélectionnés ci-dessous",
        value="AND"
    ),
    discord.SelectOption(
        label="OU",
        description="Les plongeurs ayant AU MOINS 1 des critères sélectionnés ci-dessous",
        value="OR"
    )
]