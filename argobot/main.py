import dotenv
import os
import logging

from bot_class import ArgoBot
import database




if __name__ == "__main__":
    dotenv.load_dotenv()
    TOKEN = os.getenv("ARGOBOT_TOKEN")
    PATH = os.getenv("PATH_PROJECT")


    # Date de dernier lancement du bot
    try:
        last_launched = os.path.getmtime(PATH + "pid")
    except:
        last_launched = 0
    
    # Date de dernier ajout dans les fichiers contenant les constantes
    last_modified = os.path.getmtime(PATH + "argobot/constants")


    # Pour les logs
    logger = logging.getLogger('discord')
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(filename='logs/discord.log', encoding='utf-8', mode='w')
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)

    argobot = ArgoBot()

    @argobot.event
    async def on_ready():
        tmp = await database.connexion(last_modified > last_launched)
        print("Bot en ligne")
        await tmp.close()


    argobot.run(TOKEN)
