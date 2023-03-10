import aiosqlite
from os.path import isfile
import constants.select_options as options
import constants.sql_request as sql_request

import dotenv
from os import getenv


# TODO: ContextManager ?
# https://book.pythontips.com/en/latest/context_managers.html


dotenv.load_dotenv()
PATH = getenv("PATH_PROJECT")

 
 
PATH_DB = PATH + "data/database.db"
PATH_SCRIPT_CREA = PATH + "data/creation.sql"


async def init_bd():
    """Retourne une connexion à la base de donnée.
    Si la base de donnée n'existe pas, on la créé et on la remplit avec les
    données de base.

    Retourne None en cas d'erreur.
    """
    conn = None

    # On teste maintenant car aiosqlite.connect créé le fichier s'il n'existe pas
    bdd_existe = isfile(PATH_DB)
    try:
        conn = await aiosqlite.connect(PATH_DB)
    except aiosqlite.Error as e:
        print(f"Erreur SQLite: {e}")
        return None
    

    if not bdd_existe:
        print("Création Database")
        with open(PATH_SCRIPT_CREA, 'r') as f:
            script = f.read()
            await conn.executescript(script)
        await remplissage(conn)

    return conn




async def remplissage(conn: aiosqlite.Connection):
    """Remplit la base de données avec les données de base:
    Fédérations, niveaux, intérêts, spécialités et activités professionnelles."""
    cur = await conn.cursor()

    # Insertion dans fédérations
    fede = "INSERT INTO Federation (idFederation, sigleFederation, nomCompletFederation) VALUES (?, ?, ?)"
    data = [(int(el.value), el.label, el.description) for el in options.FEDERATIONS]
    await cur.executemany(fede, data)

    # Pour les niveaux
    await cur.executescript(sql_request.REMPLISSAGE_NIVEAUX)

    # Insertion dans intérêts:
    interets = "INSERT INTO Interet (idInteret, nomInteret) VALUES (?, ?)"
    data = [(int(el.value), el.label) for el in options.INTERETS]
    await cur.executemany(interets, data)

    # Insertion dans spécialités
    specialites = "INSERT INTO Specialite (idSpecialite, nomSpecialite) VALUES (?, ?)"
    data = [(int(el.value), el.label) for el in options.SPECIALITES]
    await cur.executemany(specialites, data)
        
    # Activités pro
    activite = "INSERT INTO ActivitePro (idActivitePro, nomActivitePro) VALUES (?, ?)"
    data = [(int(el.value), el.label) for el in options.PROFESSIONS]
    await cur.executemany(activite, data)
    
    await conn.commit()
    await cur.close()
