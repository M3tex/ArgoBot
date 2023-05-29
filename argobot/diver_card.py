from os import listdir
from wand.drawing import Drawing
from wand.image import Image as Image_

import dotenv
from os import getenv


dotenv.load_dotenv()
PATH = getenv("PATH_PROJECT")
PATH += "resources/card_builder/"



def create_diver_card(plongeur, fp):
    """
    Créé la carte de plongeur. Le fond de la carte dépend du nombre de plongées.
    """
    font = "Fonts/futura.ttf"
    font2 = "Fonts/futura.ttf"
    
    nb_plongee_to_animal = {10: "Crevette", 20: "Méduse", 50: "Homard", 
                            100: "Tortue", 200: "Poisson Clown",
                            300: "Phoque", 500: "Dauphin", 1000: "Requin", 
                            2000: "Orque", 5000: "Mégalodon"}

    # Supression des caractères non supportés par la police
    new_str = ""
    for c in plongeur.prenom:
        # Pour éviter les caractères non ASCII comme les emojis
        if ord(c) <= 255:   
            new_str += c
    plongeur.prenom = new_str
        
    new_str = ""
    for c in plongeur.region:
        if ord(c) <= 255:
            new_str += c
    plongeur.region = new_str


    nb_plongees = nb_plongee_to_animal[plongeur.nombre_plongee].upper()
    data = [plongeur.prenom.upper(), plongeur.region.upper(), 
            plongeur.federations[0].nom.upper(), plongeur.niveaux[0].nom.upper(), 
            nb_plongees]
    
    offset_incr = [0, 10, 25, -3, -3, -3]
    y_offset = 185

    
    # Fond de carte en fonction du nombre de plongées
    fichier = nb_plongees if (nb_plongees + ".jpg") in listdir(PATH + "Images/") else "CREVETTE"
    with Image_(filename=PATH + f"Images/{fichier}.jpg") as image:
        with Drawing() as draw:
            draw.font_size = 62
            draw.font = PATH + font
            draw.fill_color = 'white'
            draw.text_kerning = 7.5     # Espacement entre les caractères
            draw.text_alignment = 'center'


            for i, val in enumerate(data):
                if i != 0:
                    draw.text_kerning = 3.5
                    draw.font_size = 35 if i == 1 else 41
                    y_offset += draw.get_font_metrics(image=image, text=val).text_height + offset_incr[i]
                

                draw.text(image.width // 2, int(y_offset), val)
            
            draw(image)
        image.save(file=fp)     # sauvegarde les modifications, PAS le fichier
