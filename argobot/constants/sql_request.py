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




# On se permet de formatter car les idPlongeur ne sont pas saisis par les utilisateurs
# donc pas d'injection possible.
# (entiers non signés sur 64 bits déterminés automatiquement par Discord)

SELECT_SIGLE_FEDE = """
SELECT sigleFederation 
FROM Federation F, PlongeurAffilieAFederation PF
WHERE PF.idPlongeur = {}
AND F.idFederation = PF.idFederation;
"""


SELECT_NOM_NIVEAU = """
SELECT nomNiveau 
FROM Niveau N, PlongeurPossedeNiveau PN
WHERE PN.idPlongeur = {}
AND N.idNiveau = PN.idNiveau;
"""


SELECT_NOM_SPECIALITE = """
SELECT nomSpecialite
FROM Specialite S, PlongeurPossedeSpecialite PS
WHERE PS.idPlongeur = {}
AND PS.idSpecialite = S.idSpecialite;
"""


SELECT_NOM_INTERET = """
SELECT nomInteret
FROM Interet I, PlongeurPossedeInteret PI
WHERE PI.idPlongeur = {}
AND PI.idInteret = I.idInteret;
"""


SELECT_NOM_ACTIVITE_PRO = """
SELECT nomActivitePro
FROM ActivitePro AP, PlongeurTravailleDansActivitePro PTA
WHERE PTA.idPlongeur = {}
AND PTA.idActivitePro = AP.idActivitePro;
"""


COUNT_PLONGEUR = """
SELECT count(*) FROM Plongeur;"""


COUNT_FFESSM = """
SELECT count(*) 
FROM PlongeurAffilieAFederation 
WHERE idFederation IN (
    SELECT idFederation
    FROM Federation
    WHERE sigleFederation LIKE 'FFESSM'
);
"""


COUNT_PADI = """
SELECT count(*) 
FROM PlongeurAffilieAFederation 
WHERE idFederation IN (
    SELECT idFederation
    FROM Federation
    WHERE sigleFederation LIKE 'PADI'
);
"""


COUNT_SSI = """
SELECT count(*) 
FROM PlongeurAffilieAFederation 
WHERE idFederation IN (
    SELECT idFederation
    FROM Federation
    WHERE sigleFederation LIKE 'SSI'
);
"""
