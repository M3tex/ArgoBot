"""
Contient les messages utilisés dans les réponses du bot (aide pour les menus,
messages d'erreur, messages de confirmation etc.)

La syntaxe est celle utilisée par Discord pour formatter les messages.
https://support.discord.com/hc/en-us/articles/210298617-Markdown-Text-101-Chat-Formatting-Bold-Italic-Underline-
"""



CREATION_MENU_1 = """
## Renseigne tes informations de plongeur ! :pencil: 


**Attention**: La **1ère fédération sélectionnée** sera celle affiché sur ta carte !
(*L'odre dans lequel elles sont ensuite affichées n'est pas important*)

De même pour les niveaux.
"""


CREATION_MENU_2 = """
## Renseigne tes informations de plongeur ! :pencil: 


Le champ "Rendre mes données publiques" concerne la fonction de recherche de binômes
"""

CREATION_SUCCESS = """
Les informations ont été enregistrées ! :white_check_mark: 

Tu peux maintenant faire `/infos_plongeur carte` pour obtenir **ta carte de plongeur** :identification_card:

Pour accéder, modifier ou supprimer tes informations de la base de données, utilise `/rgpd` !
"""

ABANDON_CREATION = """
**Abandonné :x:**

Vous pouvez rejetter ce message et relancer la commande si vous le souhaitez
"""


CREATION_INCOMPLET = """
## :warning:  Veuillez remplir tous les champs  :warning:
"""



PLONGEUR_INEXISTANT = """
Vous n'êtes pas dans la base de donnée.
Faites `/infos_plongeur création` pour vous enregistrer."""



HELP_PLONGEURID = """
Choisissez une commande pour afficher son aide"""


HELP_CREATION = """
## `/infos_plongeur création` 
Cette commande vous affiche un menu permettant de saisir vos informations de plongeur.
Si vous aviez déjà saisi des données, elles seront mises à jour.

Les données stockées sont:
* Votre identifiant discord (entier non signé sur 64 bits)
* Votre prénom (ou pseudo si vous renseignez votre pseudo)
* Votre nombre de plongées
* Votre région
* Une description que vous aurez renseignée (optionnelle)
* Votre pratique de la plongée (Loisir et/ou Professionelle)
* Les fédérations auxquelles vous êtes affiliés
* Les niveaux de plongée que vous possédez
* Vos intérêts en plongée (biologie, épaves & histoire, chasse, etc.)
* Vos spécialités (spécialité Nitrox, combinaison étanche, etc.)
* Votre (éventuelle) activité professionnelle dans la plongée
* Votre choix sur l'apparition dans les résultats de la recherche de binôme (oui ou non)

:bulb: Aucune de ces données n'est déterminée automatiquement (mis à part votre identifiant Discord).
Par exemple votre région n'est **pas** déterminée à partir de votre adresse IP, vous la saisissez vous même.
*(Votre adresse IP n'est même pas accessible via l'API de Discord)*

:bulb: Ces données sont en libre accès pour tous les membres de ce serveur discord (via la fonction de recherche de binôme)
*Sauf si vous avez sélectionné l'option rendant vos données cachées aux autres membres (dans ce cas notez \
que les **administrateurs** y ont quand même accès).*

:bulb: **Aucune** de ces données n'est utilisée dans un contexte extérieur au serveur Discord.

:bulb: Vous pouvez **à tout moment** supprimer vos données de la base de données en utilisant la commande:
`/infos_plongeur suppression`
"""


HELP_SUPPRESSION = """
## `/infos_plongeur suppression`
Cette commande permet de supprimer toutes les données liées à votre identifiant Discord de la base de données.
"""


HELP_CARTE = """
## `/infos_plongeur carte`
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
## :x:  Seuls les administrateurs peuvent utiliser cette commande."""


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


RECHERCHE_BINOME = """
## Bienvenue dans le menu de **recherche de binôme** :mag: !

Chaque page du menu vous permettra de filtrer le résultat par critères.
Vous pourrez changer l'opérateur indépendamment pour chaque critère.

Les opérateurs:
- `ET`: Seuls les plongeurs possédant **tous** les crtitères sélectionnés seront dans les résultats.
- `OU`: Seuls les plongeurs possédant **au moins 1** des critères sélectionnés seront dans les résultats.

*Par exemple:
Je sélectionne les fédérations PADI et FFESSM.
Si je choisis le **ET**, seulement les plongeurs affiliés à la fois à PADI **et** à la FFESSM seront présents \
dans les résultats.
Si je choisis le **OU**, les plongeurs affiliés à PADI **ou** à la FFESSM seront présents.*"""


RECHERCHE_RESULTS = """
## Voici les résultats de votre recherche

Il y a `{nb}` plongeurs correspondant à vos critères"""


RECHERCHE_CONTACT = """
## :postbox:  Vous pouvez contacter {name} en cliquant ici → <@{id}>
Il vous suffit ensuite d'appuyer sur "Envoyer un message" et d'écrire un message sympa :incoming_envelope:"""



RGPD = """
Lorsque vous utilisez la commande `/infos_plongeur création`, les données que vous renseignez sont stockées \
dans une base de données.
Le regroupement des informations renseignées (prénom ou pseudo, région, fédération, niveaux, etc.) pourrait \
être considéré comme indirectement identifiant, et on pourrait alors parler de données personnelles.

Les informations stockées se limitent à celles que vous renseignerez dans le menu de création, ainsi que votre \
identifiant Discord (un entier non signé sur 64bits). Pour voir la liste complète des données stockées, vous pouvez \
utiliser la commande `/infos_plongeur aide` puis `création`.

- Si vous souhaitez accéder à ce qui est stocké sur vous dans la base de donnée, cliquez sur le bouton \
correspondant ci-dessous.
- Si vous souhaitez modifier vos informations, réutilisez simplement la commande `/infos_plongeur création`
- Si vous souhaitez supprimer vos informations de la base de données, utilisez la commande `/infos_plongeur suppression` \
(ou cliquez sur "Mes informations" puis sur "Supprimer mes informations")

Ces données servent principalement à la fonction de recherche de binôme et à la création de votre carte de plongeur, \
elles sont donc en libre accès pour **tous** les membres de ce serveur Discord, sauf si vous avez refusé d'apparaître dans \
les résultats de recherche (dans ce cas notez toutefois que les administrateurs y ont accès)

Ces données sont susceptibles d'être utilisées pour réaliser des statistiques anonymisées (du style: `Il y a \
47% de plongeurs affiliés à la FFESSM dans le serveur`).

**Aucune** de ces données n'est utilisée dans un contexte extérieur au serveur Discord
"""


WARNING_RGPD = """
En cliquant sur "Suivant", vous acceptez que les informations que vous allez renseigner soient stockées dans une base de données.
Pour + d'information à ce sujet, utilisez `/rgpd`

*Notez qu'aucune information ne sera enregistrée avant la dernière confirmation (juste après la description optionnelle)*"""