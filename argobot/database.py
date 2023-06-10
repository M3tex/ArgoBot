import aiosqlite
from os.path import isfile
import constants.sql_request as sql_request
import yaml
import dotenv
import os

import discord

from bot_class import ArgoBot




dotenv.load_dotenv()
PATH = os.getenv("PATH_PROJECT")

 
PATH_DB = PATH + "data/database.db"
PATH_SCRIPT_CREA = PATH + "data/creation.sql"



async def connexion():
    """Retourne une connexion à la base de donnée.
    Si la base de donnée n'existe pas, on la créé et on la remplit avec les
    données "statiques".

    Retourne None en cas d'erreur.
    """
    conn = None

    # aiosqlite.connect créé le fichier s'il n'existe pas
    bdd_existe = isfile(PATH_DB)
    try:
        conn = await aiosqlite.connect(PATH_DB)
    except aiosqlite.Error as e:
        print(f"Erreur SQLite: {e}")
        await conn.close()
        return None
    
    if (not bdd_existe):
        print("Création Database")
        with open(PATH_SCRIPT_CREA, 'r') as f:
            script = f.read()
            await conn.executescript(script)
    
    # Désactivé par défaut...
    await conn.execute("PRAGMA foreign_keys=ON")

    return conn


# Car connexion utilisé dans static_data
from static_data import InfoGenerique, NiveauPlongee, Constants


# Utilisé pour les variables globales
class GlobalData:
    # Données statiques de la base de donnée
    federations: list[InfoGenerique] = []
    niveaux: list[NiveauPlongee] = []
    interets: list[InfoGenerique] = []
    specialites: list[InfoGenerique] = []
    professions: list[InfoGenerique] = []
    infostr_to_list: dict[str, list[InfoGenerique | NiveauPlongee]] = {}

    all_infos_str = ["Federation", "Niveau", "Specialite", "Interet", "Profession"]
    all_infos_pretty = ["Fédérations", "Niveaux", "Spécialités", "Intérêts", "Professions"]

    bot: ArgoBot


    def __init__(self) -> None:
        self.PATH = PATH
        self.CST = Constants()


        # todo: atexit + gestion signal kill pour fermer la connexion
        self.conn = None    # Initialisée dans async_init

        self.infostr_to_list = {
            "Federation": self.federations,
            "Niveau": self.niveaux,
            "Interet": self.interets,
            "Specialite": self.specialites,
            "Profession": self.professions
        }


    
    async def async_init(self, bot: ArgoBot):
        self.bot = bot
        self.conn = await connexion()

        await self.load_static_data()
        await self.remplissage()

        # Car problème d'importation
        self.CST.select_options.FEDERATIONS = self.get_all_options("Federation")
        self.CST.select_options.NIVEAUX = self.get_all_options("Niveau")
        self.CST.select_options.SPECIALITES = self.get_all_options("Specialite")
        self.CST.select_options.INTERETS = self.get_all_options("Interet")
        self.CST.select_options.PROFESSIONS = self.get_all_options("Profession")


        return self
    


    async def load_static_data(self):
        """
        Charge les données statiques depuis la base de données
        (Fédérations, Niveaux, Spécialités, etc.)
        """
        to_load = ["Federation", "Interet", "Specialite", "Profession"]
        to_fill = [self.federations, self.interets, self.specialites, self.professions]

        cur = await self.conn.cursor()

        for info, data in zip(to_load, to_fill):
            req = sql_request.SELECT_ALL_INFO.format(to_select=f"id{info}", info=info)
            ids = await (await cur.execute(req)).fetchall()
            for id in ids:
                data.append(await (InfoGenerique(id[0], info)).load_from_db())


        # Niveaux
        req = sql_request.SELECT_ALL_INFO.format(to_select=f"idNiveau", info="Niveau")
        ids = await (await cur.execute(req)).fetchall()
        for id in ids:
            self.niveaux.append(await NiveauPlongee(id[0]).load_from_db())

        await cur.close()
        
        return self



    def get_info_from_name(self, info: str, nom: str) -> InfoGenerique | NiveauPlongee | None:
        """
        Retourne la première information correspondante au nom passé en paramètre si
        elle existe, sinon None
        """
        to_search = self.infostr_to_list[info]
        for el in to_search:
            if el.nom == nom:
                return el
        
        return None
    


    def get_info(self, info: str, id: int):
        """
        Retourne l'information correspondante à l'id passé en paramètre si elle existe,
        sinon None
        """
        to_searh = self.infostr_to_list[info]
        for el in to_searh:
            if el.id == id:
                return el
        
        return None
    


    def get_all_options(self, info: str) -> list[discord.SelectOption]:
        """
        Retourne toutes les 'SelectOptions' correspondantes à une info.
        (Utilisées dans les menus Discord, ce sont les choix possibles)
        """
        return [x.select_option for x in self.infostr_to_list[info]
                if x.select_option != None]



    async def remplissage(self):
        """
        Remplit la base de données avec les données "statiques":
        Fédérations, niveaux, intérêts, spécialités et professions
        """
        cur = await self.conn.cursor()
        f = open(PATH + "data/remplissage.yaml", 'r')
        to_insert = yaml.load(f, Loader=yaml.FullLoader)

        # Infos ayant besoin d'être traitées séparément
        special_infos = ["Niveau"]
        
        # Pour les liens entre fédés et niveaux
        fede2id = dict()
        
        # Fédérations, intérêts, spécialités et professions
        for cat in to_insert.keys():
            if cat not in special_infos:
                for key, value in to_insert[cat].items():
                    # On insère que si n'existe pas déjà
                    existe = self.get_info_from_name(cat, key)
                    if not existe:
                        req = sql_request.INSERT_INFO.format(info=cat)
                        await cur.execute(req, (key, value["desc"]))

                    # Pour les liens entre fede et niveaux
                    if cat == "Federation":
                        fede2id[key.upper()] = cur.lastrowid if not existe else existe.id

        
        # Niveaux
        lien_niveau_fede = []
        for key, value in to_insert["Niveau"].items():
            if not self.get_info_from_name("Niveau", key):
                prof = value["prof-max-autonome"]
                desc = value["desc"]
                rang = value["rang"]
                fedes = value["fedes"]

                await cur.execute(sql_request.INSERT_NIVEAU, (key, prof, desc, rang))

                # format des tuples dans la liste: ([idFederation], idNiveau)
                # avec [idFederation] la liste des id de toutes les fédés qui proposent
                # le niveau.
                #
                # Par exemple pour l'Open Water on aurait un tuple:
                # ([idPADI, idSSI], idOpenWater)
                lien_niveau_fede.append(([fede2id[x.upper()] for x in fedes], cur.lastrowid))

        

        # Liens entre niveaux et fédérations
        for fedes, niv in lien_niveau_fede:
            for fede in fedes:
                await cur.execute(sql_request.INSERT_FEDE_NIVEAU, (fede, niv))


        await self.conn.commit()
        await cur.close()
        await self.update()
    


    async def update(self):
        """
        Recharge les informations statiques
        """
        for info in self.infostr_to_list.values():
            info.clear()

        await self.load_static_data()
