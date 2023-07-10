import dotenv
import os
from bot_class import ArgoBot
import discord
import globals
import asyncio
import os
from signal import signal, SIGUSR1


argobot: ArgoBot



def quit_bot(sig, _):
    # Pas de nettoyage à faire pour l'instant
    print("Arrêt du bot")
    loop = asyncio.get_running_loop()
    loop.create_task(argobot.arret(None))





if __name__ == "__main__":
    dotenv.load_dotenv()
    TOKEN = os.getenv("ARGOBOT_TOKEN")
    PATH = os.getenv("PATH_PROJECT")

    signal(SIGUSR1, quit_bot)


    intents = discord.Intents.default()
    intents.members = True
    globals.init()
    argobot = ArgoBot(intents=intents)


    @argobot.event
    async def on_ready():
        print("Lancement du bot...")
        print("Bot lancé")


    argobot.run(TOKEN)
