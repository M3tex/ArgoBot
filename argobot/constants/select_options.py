import discord



# * Pour les SelectOption, les `value` sont les id pour la BDD (jamais affichés à l'utilisateur)
# * A voir pour faire autrement



# ---------- Menu création plongeur ---------- #

SPECIALITES: list[discord.SelectOption] = [
    discord.SelectOption (
        label = "Pas de spécialités",
        description = "Je n'ai pas de spécialités",
        value = "0"
    ),
    discord.SelectOption (
        label = "Qualification Nitrox",
        description = "Je peux plonger au Nitrox jusqu'à 40% d'O2",
        value = "1"
    ),
    discord.SelectOption (
        label = "Qualification Nitrox Avancé",
        description = "Je peux plonger au Nitrox à + de 40% d'O2",
        value = "2"
    ),
    discord.SelectOption (
        label = "Qualification combinaison étanche",
        description = "Je suis qualifié pour plonger en combinaison étanche",
        value = "3"
    ),
    discord.SelectOption (
        label = "Qualification Recycleur",
        description = "Je suis qualifié pour plonger avec un recycleur",
        value = "4"
    ),
    discord.SelectOption (
        label = "Qualification TriMix",
        description = "Je suis qualifié pour plonger avec un mélange contenant de l'Helium",
        value = "5"
    ),
    discord.SelectOption (
        label = "Qualification TriMix Avancé",
        description = "",
        value = "6"
    ),
    discord.SelectOption (
        label = "Qualification Sidemount",
        description = "Je suis qualifié pour plonger en configuration Sidemount",
        value = "7"
    ),
    discord.SelectOption (
        label = "Formation Secourisme",
        description = "J'ai suivi une formation de secourisme spécifique à la plongée",
        value = "8"
    ),
    discord.SelectOption (
        label = "Wetsuit Filler",
        description = "Nan, je n'ai pas pissé dans ma combi...",
        value = "9"
    )
]



# TODO: Voir avec les gens pour rajouter d'autres intérêts
INTERETS: list[discord.SelectOption] = [
    discord.SelectOption (
        label = "Chasse sous marine",
        description = "Je pratique la chasse sous marine",
        value = "0"
    ),
    discord.SelectOption (
        label = "Biologie",
        description = "Je m'intéresse beaucoup à la vie sous marine !",
        value = "1"
    ),
    discord.SelectOption (
        label = "Epaves & Histoire",
        description = "Les épaves et leurs histoires me fascinent",
        value = "2"
    ),
    discord.SelectOption (
        label = "Photo / Vidéo",
        description = "Ma passion c'est l'image !",
        value = "3"
    ),
    discord.SelectOption (
        label = "Apnée",
        description = "Je pratique l'apnée",
        value = "4"
    ),
    discord.SelectOption (
        label = "Plongée Sportive",
        description = "Je pratique la plongée sportive",
        value = "5"
    ),
    discord.SelectOption (
        label = "Milieu Associatif",
        description = "Je suis actif au sein d'une association",
        value = "6"
    )
]


# TODO: Voir avec les gens pour rajouter des professions
PROFESSIONS: list[discord.SelectOption] = [
    discord.SelectOption (
        label = "Instructeur de plongée",
        description = "J'enseigne la plongée",
        value = "0"
    ),
    discord.SelectOption (
        label = "Biologiste",
        description = "J'étudie la vie marine",
        value = "1"
    ),
    discord.SelectOption (
        label = "Archéologue",
        description = "Je participe à des fouilles sous-marines",
        value = "2"
    ),
    discord.SelectOption (
        label = "Cadreur sous-marin",
        description = "Je vis de la vidéo sous-marine",
        value = "3"
    ),
    discord.SelectOption (
        label = "Scaphandrier",
        description = "J'aime bien avoir la tête au sec !",
        value = "4"
    ),
    discord.SelectOption (
        label = "Centre de plongée",
        description = "Je possède / gère un centre de plongée",
        value = "5"
    ),
    discord.SelectOption (
        label = "Médecin Hyperbare",
        description = "Je m'y connais en bubulles !",
        value = "6"
    )
]



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



##### Fédérations et Niveaux #####
FEDERATIONS: list[discord.SelectOption] = [
    discord.SelectOption (
        label = "FFESSM",
        description = "Fédération Française d'Etude et de Sports Sous-Marins",
        emoji = "<:ffessm:1071852021533122651>",
        value = "0"
    ),
    discord.SelectOption (
        label = "PADI",
        description = "Professional Association of Diving Instructors",
        emoji = "<:padi:1071851979338436741>",
        value = "1"
    ),
    discord.SelectOption (
        label = "SSI",
        description = "Scuba Schools International",
        emoji = "<:ssi:1071851925710061598>",
        value = "2"
    ),
    discord.SelectOption (
        label = "ANMP",
        description = "Association Nationale des Moniteurs de Plongée",
        emoji = "<:anmp:1088502169218580581>",
        value = "3"
    )
]



### ------- Niveaux ------- ###

# `value` -> idNiveau:idFede:profMaxAutonomie

NIVEAUX_FFESSM: list[discord.SelectOption] = [
    discord.SelectOption (
        label = "Niveau 1",
        description = "Encadré à 20m",
        value = "0:0:0"
    ),
    discord.SelectOption (
        label = "Niveau 2",
        description = "Autonome 20m, encadré 40m",
        value = "1:0:20"
    ),
    discord.SelectOption (
        label = "Niveau 3",
        description = "Autonome 60m",
        value = "2:0:60"
    ),
    discord.SelectOption (
        label = "Niveau 4",
        description = "Autonome 60, Guide de Palanquée",
        value = "3:0:60"
    ),
    discord.SelectOption (
        label = "Niveau 5",
        description = "Directeur de Plongée",
        value = "4:0:60"
    )
]



NIVEAUX_PADI: list[discord.SelectOption] = [
    discord.SelectOption (
        label = "Open Water Diver",
        value = "5:1:18"
    ),
    discord.SelectOption (
        label = "Adventure Diver",
        value = "6:1:18"
    ),
    discord.SelectOption (
        label = "Advanced Open Water",
        value = "7:1:30"
    ),
    discord.SelectOption (
        label = "Deep diver",
        value = "8:1:40"
    ),
    discord.SelectOption (
        label = "Dive Master",
        value = "9:1:40"
    ),
    discord.SelectOption (
        label = "Instructor",
        value = "10:1:40"
    )
]


# TODO: Voir les différences SSI & PADI (pas de différence dans les intitulés de ce que j'ai compris)
NIVEAUX_SSI: list[discord.SelectOption] = [
    discord.SelectOption (
        label = "Open Water Diver",
        value = "5:2:18"
    ),
    discord.SelectOption (
        label = "Adventure Diver",
        value = "6:2:18"
    ),
    discord.SelectOption (
        label = "Advanced Open Water",
        value = "7:2:30"
    ),
    discord.SelectOption (
        label = "Deep diver",
        value = "8:2:40"
    ),
    discord.SelectOption (
        label = "Dive Master",
        value = "9:2:40"
    ),
    discord.SelectOption (
        label = "Instructor",
        value = "10:2:40"
    )
]


NIVEAUX_ANMP: list[discord.SelectOption] = [
    discord.SelectOption (
        label = "Niveau 1",
        description = "Encadré à 20m",
        value = "0:3:0"
    ),
    discord.SelectOption (
        label = "Niveau 2",
        description = "Autonome 20m, encadré 40m",
        value = "1:3:20"
    ),
    discord.SelectOption (
        label = "Niveau 3",
        description = "Autonome 60m",
        value = "2:3:60"
    ),
    discord.SelectOption (
        label = "Niveau 4",
        description = "Autonome 60, Guide de Palanquée",
        value = "3:3:60"
    ),
    discord.SelectOption (
        label = "Niveau 5",
        description = "Directeur de Plongée",
        value = "4:3:60"
    )
]


NIVEAUX = NIVEAUX_FFESSM + NIVEAUX_PADI + NIVEAUX_SSI + NIVEAUX_ANMP



### Consentement apparition résultats recherche binome
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




### Nombre de plongées
# ! Ne pas oublier d'ajouter les emojis custom (voir si possible automatiquement via le bot ?)
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