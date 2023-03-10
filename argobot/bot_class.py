import discord
from configparser import ConfigParser


import dotenv
from os import getenv


dotenv.load_dotenv()
PATH = getenv("PATH_PROJECT")


PATH_SETTINGS = PATH + 'settings.ini'



# Sous-Classe pour le bot
class ArgoBot(discord.Bot):

    def __init__(self, description=None, *args, **options):
        super().__init__(description, *args, **options)

        self.load_extension('cogs.infos_plongeur')
        self.load_extension('cogs.admin')


        # On récupère les données contenues dans le fichier de configuration
        self.settings = ConfigParser()
        self.settings.read(PATH_SETTINGS)


    

    def is_infos_plongeur_locked(self):
        return self.settings['bot-settings'].getboolean('is_infos_plongeur_locked')


    def is_cards_locked(self):
        return self.settings['bot-settings'].getboolean('is_cards_locked')


    def __update_settings_file(self):
        with open(PATH_SETTINGS, 'w') as cfg:
            self.settings.write(cfg)


    def lock_infos_plongeur(self):
        if self.is_infos_plongeur_locked(): 
            return  # Evite d'écrire dans le fichier pour rien
        
        self.settings['bot-settings']['is_infos_plongeur_locked'] = 'True'
        self.__update_settings_file()
    
    def unlock_infos_plongeur(self):
        if not self.is_infos_plongeur_locked(): 
            return  # Evite d'écrire dans le fichier pour rien
        
        self.settings['bot-settings']['is_infos_plongeur_locked'] = 'False'
        self.__update_settings_file()
    


    def lock_cards(self):
        if self.is_cards_locked(): 
            return  # Evite d'écrire dans le fichier pour rien
        
        self.settings['bot-settings']['is_cards_locked'] = 'True'
        self.__update_settings_file()
        
    
    def unlock_cards(self):
        if not self.is_cards_locked(): 
            return  # Evite d'écrire dans le fichier pour rien
        
        self.settings['bot-settings']['is_cards_locked'] = 'False'
        self.__update_settings_file()
