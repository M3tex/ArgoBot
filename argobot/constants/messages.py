


MENU_1 = """
:pencil: Remplis tes informations de plongeur !

**Attention**: La **1ère fédération sélectionnée** sera celle affiché sur ta carte !
(*L'odre dans lequel elles sont ensuite affichées n'est pas important*)

De même pour les niveaux.
"""

MENU_2 = """
:pencil: Remplis tes informations de plongeur !

Le champ "Rendre mes données publiques" concerne la fonction de recherche de binômes
"""

CREATION_SUCCESS = """
:white_check_mark: Les informations ont été enregistrées !

Tu peux maintenant faire `/infos_plongeur carte` pour obtenir ta carte de plongeur :identification_card:
"""

ABANDON_CREATION = """
**Abandonné :x:**

Vous pouvez rejetter ce message et relancer la commande si vous le souhaitez
"""


CREATION_INCOMPLET = """
**:warning:  Veuillez remplir tous les champs  :warning:**\n"""



PLONGEUR_INEXISTANT = """
Vous n'êtes pas dans la base de donnée.
Faites `/infos_plongeur création` pour vous enregistrer."""



HELP_PLONGEURID = """
Choisissez une commande pour afficher son aide"""


HELP_CREATION = """
`/infos_plongeur création` 
Cette commande vous affiche un menu permettant de saisir vos informations de plongeur.
Si vous aviez déjà saisi des données, elles seront mises à jour.

Les données stockées sont:
    **→** Votre identifiant discord
    **→** Votre prénom (ou pseudo si vous renseignez votre pseudo)
    **→** Votre nombre de plongées
    **→** Votre région
    **→** Une description que vous aurez renseignée (optionnelle)
    **→** Votre pratique de la plongée (Loisir et/ou Professionelle)
    **→** Les fédérations auxquelles vous êtes affiliés
    **→** Les niveaux de plongée que vous possédez
    **→** Vos intérêts en plongée (biologie, épaves & histoire, chasse, etc.)
    **→** Vos spécialités (spécialité Nitrox, combinaison étanche, etc.)
    **→** Votre (éventuelle) activité professionnelle dans la plongée

:bulb: Aucune de ces données n'est déterminée automatiquement (mis à part votre identifiant Discord).
Par exemple votre région n'est **pas** déterminée à partir de votre adresse IP, vous la saisissez vous même.
*(Votre adresse IP n'est même pas accessible via l'API de Discord)*

:bulb: Ces données sont en libre accès pour tous les membres de ce serveur discord (via la fonction de recherche de binôme)
*Sauf si vous avez sélectionné l'option rendant vos données cachées aux autres membres (dans ce cas notez que les **administrateurs** y ont quand même accès).*

:bulb: **Aucune** de ces données n'est utilisée dans un contexte extérieur au serveur Discord.

:bulb: Vous pouvez **à tout moment** supprimer vos données de la base de données en utilisant la commande:
`/infos_plongeur suppression`
"""


HELP_SUPPRESSION = """
`/infos_plongeur suppression`
Cette commande permet de supprimer toutes les données liées à votre identifiant Discord de la base de données.
"""


HELP_CARTE = """
`/infos_plongeur carte`
Cette commande permet d'afficher **votre** carte de plongeur (visible seulement par vous).
Cette carte est générée à partir des informations renseignées via `/infos_plongeur création`

Les designs ont été réalisés par Argonaute et certaines images proviennent de la communauté !"""


ADMIN_LOCKED_CARDS = """
:bulb: Les envois de cartes sont désactivées pour **tout le monde** !"""


ADMIN_UNLOCKED_CARDS = """
:identification_card: Les envois de cartes sont de nouveau opérationnels !"""


ADMIN_LOCKED_DB = """
:lock: Les modifications de la base de données sont désactivées !"""


ADMIN_UNLOCKED_DB = """
:memo: Les modifications de la base de données sont de nouveau opérationnelles"""


NOT_ADMIN = """
Seuls les administrateurs peuvent utiliser cette commande."""


INFO_CREA_LOCKED = """
Les saisies / modifications d'informations ne sont pas autorisées pour le moment.
Le système de saisie est probablement en maintenance :construction:

*Si le problème persiste, renseignez-vous auprès d'un administrateur*"""



INFO_CARD_LOCKED = """
Les cartes de plongeur ne sont pas disponibles pour le moment.
Le système de création des cartes est probablement en maintenance :construction:


*Si le problème persiste, renseignez-vous auprès d'un administrateur*"""


SUPPRESSION_PLONGEUR = """
L'utilisateur `{}` a bien été supprimé de la base de données."""


STATS_PLONGEUR_FEDE = """
- Il y a `{ffessm_count}` plongeurs affiliés à la FFESSM (`{ffessm_percentage:.2f}%`)
- Il y a `{padi_count}` plongeurs affiliés à PADI (`{padi_percentage:.2f}%`)
- Il y a `{ssi_count}` plongeurs affiliés à SSI (`{ssi_percentage:.2f}%`)

*Notez qu'un plongeur peut-être affilié à plusieurs fédérations*
"""