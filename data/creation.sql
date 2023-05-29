-- Script de création de la base


-- Entités
CREATE TABLE IF NOT EXISTS Plongeur (
    -- Car id Discord sur 64 bits
    idPlongeur UNISGNED BIG INT PRIMARY KEY,   
    prenom VARCHAR(50) NOT NULL,
    nombrePlongee INT NOT NULL,
    region VARCHAR(50) NOT NULL,
    description TEXT,
    pratique VARCHAR(20),
    consent INT NOT NULL
);


CREATE TABLE IF NOT EXISTS Federation (
    idFederation INTEGER PRIMARY KEY,
    nomFederation VARCHAR(20),
    descriptionFederation VARCHAR(100)
);


CREATE TABLE IF NOT EXISTS Niveau (
    idNiveau INTEGER PRIMARY KEY,
    nomNiveau VARCHAR(50) NOT NULL,
    profondeurMaxAutonomie INT NOT NULL,
    descriptionNiveau TEXT,

    -- Pour "trier" les niveaux: N3 > N1, N3 > Open Water, etc.
    -- en flottant pour si besoin de subtilité / ajustements
    rang REAL NOT NULL
);



CREATE TABLE IF NOT EXISTS Interet (
    idInteret INTEGER PRIMARY KEY,
    nomInteret VARCHAR(50) NOT NULL,
    descriptionInteret TEXT
);


CREATE TABLE IF NOT EXISTS Specialite (
    idSpecialite INTEGER PRIMARY KEY,
    nomSpecialite VARCHAR(50) NOT NULL,
    descriptionSpecialite TEXT
);


CREATE TABLE IF NOT EXISTS Profession (
    idProfession INTEGER PRIMARY KEY,
    nomProfession VARCHAR(50) NOT NULL,
    descriptionProfession TEXT
);


-- Liens n:m
CREATE TABLE IF NOT EXISTS FederationPossedeNiveau (
    idFederation REFERENCES Federation ON DELETE CASCADE,
    idNiveau REFERENCES Niveau ON DELETE CASCADE,

    PRIMARY KEY(idFederation, idNiveau)
);


CREATE TABLE IF NOT EXISTS PlongeurPossedeFederation (
    idPlongeur REFERENCES Plongeur ON DELETE CASCADE,
    idFederation REFERENCES Federation ON DELETE CASCADE,

    PRIMARY KEY(idPlongeur, idFederation)
);


CREATE TABLE IF NOT EXISTS PlongeurPossedeNiveau (
    idPlongeur REFERENCES Plongeur ON DELETE CASCADE,
    idNiveau REFERENCES Niveau ON DELETE CASCADE,

    PRIMARY KEY(idPlongeur, idNiveau)
);


CREATE TABLE IF NOT EXISTS PlongeurPossedeInteret (
    idPlongeur REFERENCES Plongeur ON DELETE CASCADE,
    idInteret REFERENCES Interet ON DELETE CASCADE,

    PRIMARY KEY(idPlongeur, idInteret)
);


CREATE TABLE IF NOT EXISTS PlongeurPossedeSpecialite (
    idPlongeur REFERENCES Plongeur ON DELETE CASCADE,
    idSpecialite REFERENCES Specialite ON DELETE CASCADE,

    PRIMARY KEY(idPlongeur, idSpecialite)
);


CREATE TABLE IF NOT EXISTS PlongeurPossedeProfession (
    idPlongeur REFERENCES Plongeur ON DELETE CASCADE,
    idProfession REFERENCES Profession ON DELETE CASCADE,

    PRIMARY KEY(idPlongeur, idProfession)
);

/*
TODO: Triggers à faire (même si en principe tout est déjà bon avant insertion)

    - Quand on insère dans PlongeurPossedeNiveau, vérifier que le plongeur soit affilié à la fede
    - Quand on insère dans PlongeurTravailleDansActivitePro, vérifier que le plongeur soit en pratique Pro

TODO: Fonction à faire

    - Calculer la profondeur maximale (avec les niveau possédés)
*/