import dotenv
import os
import logging

from bot_class import ArgoBot


# Pour les logs
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='logs/discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)




if __name__ == "__main__":
    dotenv.load_dotenv()
    TOKEN = os.getenv("ARGOBOT_TOKEN")

    argobot = ArgoBot()

    @argobot.event
    async def on_ready():
        print("Bot en ligne")


    argobot.run(TOKEN)
