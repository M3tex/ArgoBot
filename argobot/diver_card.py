from os import listdir
from wand.drawing import Drawing
from wand.image import Image as Image_

import dotenv
from os import getenv


dotenv.load_dotenv()
PATH = getenv("PATH_PROJECT")
PATH += "resources/card_builder/"



def create_diver_card(nom: str, region: str, fede: str, niveau: str, nb_plongees: str, fp):
    font = "Fonts/futura.ttf"
    font2 = "Fonts/futura.ttf"

    data = [nom.upper(), region.upper(), fede.upper(), niveau.upper(), nb_plongees.upper()]
    offset_incr = [0, 10, 25, -3, -3, -3]
    y_offset = 185

    
    fichier = nb_plongees.upper() if (nb_plongees.upper() + ".jpg") in listdir(PATH + "Images/") else "CREVETTE"
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
