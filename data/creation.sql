-- Script de création de la base


-- Entités
CREATE TABLE IF NOT EXISTS Plongeur (
    -- Car id Discord sur 18 chiffres, log10(MAX_UBIGINT) ~= 19
    idPlongeur UNISGNED BIG INT PRIMARY KEY,   
    prenom VARCHAR(50) NOT NULL,
    nombrePlongee INT NOT NULL,
    region VARCHAR(50) NOT NULL,
    description TEXT,
    pratique VARCHAR(20),
    consent INT NOT NULL
);


-- ! Pour PADI et SSI si les niveaux sont exactement les mêmes
CREATE TABLE IF NOT EXISTS Federation (
    idFederation INT PRIMARY KEY,
    sigleFederation VARCHAR(20),
    nomCompletFederation VARCHAR(100)
);


CREATE TABLE IF NOT EXISTS Niveau (
    idNiveau INT PRIMARY KEY,
    nomNiveau VARCHAR(50) NOT NULL,
    nomCourtNiveau VARCHAR(20) NOT NULL,
    profondeurMaxAutonomie INT NOT NULL,
    idFederation INT REFERENCES Federation
);


CREATE TABLE IF NOT EXISTS Interet (
    idInteret INT PRIMARY KEY,
    nomInteret VARCHAR(50) NOT NULL
);


CREATE TABLE IF NOT EXISTS Specialite (
    idSpecialite INT PRIMARY KEY,
    nomSpecialite VARCHAR(50) NOT NULL
);


CREATE TABLE IF NOT EXISTS ActivitePro (
    idActivitePro INT PRIMARY KEY,
    nomActivitePro VARCHAR(50) NOT NULL
);


-- Liens n:m
CREATE TABLE IF NOT EXISTS PlongeurAffilieAFederation (
    idPlongeur REFERENCES Plongeur,
    idFederation REFERENCES Federation,

    PRIMARY KEY(idPlongeur, idFederation)
);


CREATE TABLE IF NOT EXISTS PlongeurPossedeNiveau (
    idPlongeur REFERENCES Plongeur,
    idNiveau REFERENCES Niveau,

    PRIMARY KEY(idPlongeur, idNiveau)
);


CREATE TABLE IF NOT EXISTS PlongeurPossedeInteret (
    idPlongeur REFERENCES Plongeur,
    idInteret REFERENCES Interet,

    PRIMARY KEY(idPlongeur, idInteret)
);


CREATE TABLE IF NOT EXISTS PlongeurPossedeSpecialite (
    idPlongeur REFERENCES Plongeur,
    idSpecialite REFERENCES Specialite,

    PRIMARY KEY(idPlongeur, idSpecialite)
);


CREATE TABLE IF NOT EXISTS PlongeurTravailleDansActivitePro (
    idPlongeur REFERENCES Plongeur,
    idActivitePro REFERENCES ActivitePro,

    PRIMARY KEY(idPlongeur, idActivitePro)
);

/*
TODO: Triggers à faire (même si en principe tout est déjà bon avant insertion)

    - Quand on insère dans PlongeurPossedeNiveau, vérifier que le plongeur soit affilié à la fede
    - Quand on insère dans PlongeurTravailleDansActivitePro, vérifier que le plongeur soit en pratique Pro

TODO: Fonction à faire

    - Calculer la profondeur maximale (avec les niveau possédés)
*/