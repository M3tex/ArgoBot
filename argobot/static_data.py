import discord

import constants.messages as messages
import constants.select_options as select_options
import constants.sql_request as requests
from database import connexion


class Constants:
    def __init__(self):
        self.messages = messages
        self.select_options = select_options
        self.requests = requests

        
    

class InfoGenerique:
    nom = ""
    description = ""
    select_option: discord.SelectOption = None

    # Pour les SelectOption
    _label2emoji = {
        "ffessm": "<:ffessm:1071852021533122651>",
        "padi": "<:padi:1071851979338436741>",
        "ssi": "<:ssi:1071851925710061598>",
        "anmp": "<:anmp:1088502169218580581>",
        "loisir": "🏝️",
        "professionnel": "💵"
    }


    def __init__(self, id: int, info: str):
        self.id = id
        self.info = info



    async def load_from_db(self):
        """
        Charge les données depuis la base de données (via l'id)
        """
        conn = await connexion()
        cur = await conn.cursor()
        req = requests.SELECT_INFO.format(info=self.info)
        result = await (await cur.execute(req, (self.id, ))).fetchone()

        if result:
            self.nom = result[1]
            self.description = result[2]

            self.select_option = discord.SelectOption(
                label=self.nom,
                description=self.description,
                emoji=self._label2emoji.get(self.nom.lower(), None),
                value=str(self.id)
            )

    
        await cur.close()
        await conn.close()
        return self
    

    # Appelées quand str() est utilisé (ou quand objet passé en paramètre de print()).
    # Utile pour debug principalement
    def __str__(self):
        # Par exemple: "Qualification Nitrox (Spécialité)"
        return f"{self.nom} ({self.info})"

    def __repr__(self):
        return str(self)
    

    

class NiveauPlongee(InfoGenerique):
    # Ordre sert à comparer les niveaux (N3 > N1 par exemple, ou N3 > OW)
    # en flottant (si besoin de subtilité / ajustements)
    __ordre: float = -1
    profondeur_max: int = -1
    federations: list[int]= []

    def __init__(self, id: int):
        super().__init__(id, info="Niveau")

        
    

    async def load_from_db(self):
        """
        Charge les données depuis la base de données (via l'id)
        """
        conn = await connexion()
        cur = await conn.cursor()

        req = requests.SELECT_INFO.format(info=self.info)
        result = await (await cur.execute(req, (self.id, ))).fetchone()

        self.nom = result[1]
        self.profondeur_max = result[2]
        self.description = result[3]
        self.__ordre = result[4]

        # Les fédérations qui proposent ce niveau
        req = requests.SELECT_FEDES_DE_NIVEAU
        result = await (await cur.execute(req, (self.id, ))).fetchall()
        self.federations = [x[0] for x in result]

        await cur.close()
        await conn.close()

        self.select_option = discord.SelectOption(
            label=self.nom,
            description=self.description,
            emoji=self._label2emoji.get(self.nom, None),
            value=str(self.id)
        )

        return self     # Car utilisé comme init async

    
    # Pour comparer les niveaux
    def __lt__(self, other):
        return self.__ordre < other.__ordre
    
    def __le__(self, other):
        return self.__ordre <= other.__ordre

    def __gt__(self, other):
        return self.__ordre > other.__ordre
    
    def __ge__(self, other):
        return self.__ordre >= other.__ordre

    def __eq__(self, other):
        return self.__ordre == other.__ordre
    
    def __ne__(self, other):
        return self.__ordre != other.__ordre
