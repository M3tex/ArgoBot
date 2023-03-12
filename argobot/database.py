import aiosqlite
from os.path import isfile
import constants.select_options as options
import constants.sql_request as sql_request

import dotenv
import os


# TODO: ContextManager ?
# https://book.pythontips.com/en/latest/context_managers.html


dotenv.load_dotenv()
PATH = os.getenv("PATH_PROJECT")

 
PATH_DB = PATH + "data/database.db"
PATH_SCRIPT_CREA = PATH + "data/creation.sql"
    


async def connexion(force_remplissage = False):
    """Retourne une connexion à la base de donnée.
    Si la base de donnée n'existe pas, on la créé et on la remplit avec les
    données "statiques".

    Retourne None en cas d'erreur.
    """
    conn = None

    # On teste maintenant car aiosqlite.connect créé le fichier s'il n'existe pas
    bdd_existe = isfile(PATH_DB)
    try:
        conn = await aiosqlite.connect(PATH_DB)
    except aiosqlite.Error as e:
        print(f"Erreur SQLite: {e}")
        await conn.close()
        return None
    

    if (not bdd_existe):
        force_remplissage = True
        print("Création Database")
        with open(PATH_SCRIPT_CREA, 'r') as f:
            script = f.read()
            await conn.executescript(script)
    
    if force_remplissage:
        await remplissage(conn)

    return conn



async def remplissage(conn: aiosqlite.Connection):
    """Remplit la base de données avec les données "statiques":
    Fédérations, niveaux, intérêts, spécialités et activités professionnelles."""
    cur = await conn.cursor()

    # Pour chaque donnée "statique" on insère que si elle n'est pas déjà dans la base
    fede = "INSERT OR IGNORE INTO Federation (idFederation, sigleFederation, nomCompletFederation) VALUES (?, ?, ?)"
    data = [(int(el.value), el.label, el.description) for el in options.FEDERATIONS]
    await cur.executemany(fede, data)

    # Pour les niveaux
    # TODO: Passer par les options pour permettre de rajouter des niveaux facilement
    await cur.executescript(sql_request.REMPLISSAGE_NIVEAUX)

    # Insertion dans intérêts:
    interets = "INSERT OR IGNORE INTO Interet (idInteret, nomInteret) VALUES (?, ?)"
    data = [(int(el.value), el.label) for el in options.INTERETS]
    await cur.executemany(interets, data)

    # Insertion dans spécialités
    specialites = "INSERT OR IGNORE INTO Specialite (idSpecialite, nomSpecialite) VALUES (?, ?)"
    data = [(int(el.value), el.label) for el in options.SPECIALITES]
    await cur.executemany(specialites, data)
        
    # Activités pro
    activite = "INSERT OR IGNORE INTO ActivitePro (idActivitePro, nomActivitePro) VALUES (?, ?)"
    data = [(int(el.value), el.label) for el in options.PROFESSIONS]
    await cur.executemany(activite, data)
    
    await conn.commit()
    await cur.close()
