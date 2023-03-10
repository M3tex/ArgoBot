# TODO: Le passer en auto depuis constants.select_options comme les autres
# ! Aucun niveau pour SSI pour l'instant (car les mêmes que PADI)
# Voir si il y a des niveaux spécifiques à PADI
REMPLISSAGE_NIVEAUX = """
INSERT INTO Niveau (idNiveau, nomNiveau, nomCourtNiveau, profondeurMaxAutonomie, idFederation)
VALUES 
    (0, 'Niveau 1', 'N1', 0, 0),
    (1, 'Niveau 2', 'N2', 20, 0),
    (2, 'Niveau 3', 'N3', 60, 0), 
    (3, 'Niveau 4', 'N4', 60, 0),
    (4, 'Niveau 5', 'N5', 60, 0),
    (5, 'Open Water Diver', 'Open Water', 18, 1),
    (6, 'Adventure Diver', 'Adventure Diver', 18, 1),
    (7, 'Advanced Open Water', 'Advanced Diver', 30, 1),
    (8, 'Deep Diver', 'Deep Diver', 40, 1),
    (9, 'Dive Master', 'Dive Master', 40, 1),
    (10, 'Instructor', 'Instructor', 40, 1);
"""


INSERT_PLONGEUR = """
INSERT INTO Plongeur (idPlongeur, prenom, nombrePlongee, region, description, pratique, consent)
VALUES (:idPlongeur, :prenom, :nombrePlongees, :region, :description, :pratique, :consent);
"""


INSERT_PLONGEURFEDE = """
INSERT INTO PlongeurAffilieAFederation (idPlongeur, idFederation) VALUES (?, ?)"""


INSERT_PLONGEURNIVEAU = """
INSERT INTO PlongeurPossedeNiveau (idPlongeur, idNiveau) VALUES (?, ?)"""


INSERT_PLONGEURINTERET = """
INSERT INTO PlongeurPossedeInteret (idPlongeur, idInteret) VALUES (?, ?)"""


INSERT_PLONGEURSPECIALITE = """
INSERT INTO PlongeurPossedeSpecialite (idPlongeur, idSpecialite) VALUES (?, ?)"""


INSERT_PLONGEURACTIVITE = """
INSERT INTO PlongeurTravailleDansActivitePro (idPlongeur, idActivitePro) VALUES (?, ?)"""


INSERT_REQUESTS = [INSERT_PLONGEURFEDE, INSERT_PLONGEURNIVEAU, 
                   INSERT_PLONGEURINTERET, INSERT_PLONGEURSPECIALITE, INSERT_PLONGEURACTIVITE]


DELETE_PLONGEUR = """
DELETE FROM Plongeur WHERE idPlongeur = ?"""


DELETE_PLONGEURFEDE = """
DELETE FROM PlongeurAffilieAFederation WHERE idPlongeur = ?"""


DELETE_PLONGEURNIVEAU = """
DELETE FROM PlongeurPossedeNiveau WHERE idPlongeur = ?"""

DELETE_PLONGEURINTERET = """
DELETE FROM PlongeurPossedeInteret WHERE idPlongeur = ?"""

DELETE_PLONGEURSPECIALITE = """
DELETE FROM PlongeurPossedeSpecialite WHERE idPlongeur = ?"""

DELETE_PLONGEURACTIVITE = """
DELETE FROM PlongeurTravailleDansActivitePro WHERE idPlongeur = ?"""


DELETE_REQUESTS = [DELETE_PLONGEUR, DELETE_PLONGEURFEDE, DELETE_PLONGEURNIVEAU, 
                   DELETE_PLONGEURINTERET, DELETE_PLONGEURSPECIALITE, DELETE_PLONGEURACTIVITE]



SELECT_PLONGEUR = """
SELECT * FROM Plongeur WHERE idPlongeur = ?"""

SELECT_PLONGEURFEDE = """
SELECT idFederation FROM PlongeurAffilieAFederation WHERE idPlongeur = ?"""

SELECT_PLONGEURNIVEAU = """
SELECT idNiveau FROM PlongeurPossedeNiveau WHERE idPlongeur = ?"""

SELECT_PLONGEURINTERET = """
SELECT idInteret FROM PlongeurPossedeInteret WHERE idPlongeur = ?"""

SELECT_PLONGEURSPECIALITE = """
SELECT idSpecialite FROM PlongeurPossedeSpecialite WHERE idPlongeur = ?"""

SELECT_PLONGEURACTIVITE = """
SELECT idActivitePro FROM PlongeurTravailleDansActivitePro WHERE idPlongeur = ?"""

SELECT_REQUESTS = [SELECT_PLONGEURFEDE, SELECT_PLONGEURNIVEAU, SELECT_PLONGEURINTERET, SELECT_PLONGEURSPECIALITE, SELECT_PLONGEURACTIVITE]