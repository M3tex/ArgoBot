SELECT_PLONGEUR = """
SELECT * FROM Plongeur WHERE idPlongeur = ?"""


# On se permet de formatter les valeurs sans injection possible
# (les valeurs qui seront insérées ne sont pas modifiables par les utilisateurs)
# ici info sera forcément dans ["Federation", "Niveau", "Specialite", "Interet", "Profession"]
SELECT_INFO = """
SELECT *
FROM {info}
WHERE id{info} = ?;
"""


SELECT_ALL_INFO = """
SELECT {to_select}
FROM {info};
"""


SELECT_PLONGEUR_POSSEDE_INFO = """
SELECT id{info}
FROM PlongeurPossede{info}
WHERE idPlongeur = ?;
"""


INSERT_INFO = """
INSERT INTO {info} (nom{info}, description{info})
VALUES (?, ?);
"""

INSERT_NIVEAU = """
INSERT INTO NIVEAU (nomNiveau, profondeurMaxAutonomie, descriptionNiveau, rang)
VALUES (?, ?, ?, ?);
"""

INSERT_FEDE_NIVEAU = """
INSERT INTO FederationPossedeNiveau (idFederation, idNiveau)
VALUES (?, ?)"""


SELECT_FEDES_DE_NIVEAU = """
SELECT *
FROM FederationPossedeNiveau
WHERE idNiveau = ?;
"""


INSERT_PLONGEUR_POSSEDE_INFO = """
INSERT INTO PlongeurPossede{info} (idPlongeur, id{info})
VALUES (?, ?);
"""


INSERT_PLONGEUR = """
INSERT INTO Plongeur (idPlongeur, prenom, nombrePlongee, region, description, pratique, consent)
VALUES (:idPlongeur, :prenom, :nombrePlongees, :region, :description, :pratique, :consent);
"""