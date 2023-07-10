import discord
import aiohttp
import discord.ext.pages as pages
import flag

from highcharts_core.chart import Chart
import highcharts_core.options as hco
from highcharts_core.options.axes.title import AxisTitle




class MenuChoixVille(discord.ui.View):
    def __init__(self, villes: list[dict], complet: bool):
        super().__init__()
        self.add_item(ChoixVille(villes))
        self.complet = complet


# Si plusieurs villes avec le même nom, ce menu permettra à l'utilisateur de
# choisir la ville qui l'intéresse.
class ChoixVille(discord.ui.Select):
    view: MenuChoixVille

    def __init__(self, villes: list[dict]):
        options = []
        for i, ville in enumerate(villes):
            tmp = ville.get('admin1', None)

            opt = discord.SelectOption(
                label=ville['name'],
                emoji=flag.flag(ville['country_code']),
                description=tmp if tmp else ville['country'],
                value=str(i)
            )

            options.append(opt)


        super().__init__(
            placeholder="Choisissez la ville correspondante",
            min_values=1,
            max_values=1,
            row=0,
            options=options
        )

        self.villes = villes
        


    async def callback(self, interaction: discord.Interaction):
        # On récupère: latitude, longitude, nom_ville, code_pays
        ville = self.villes[int(self.values[0])]
        lat = ville['latitude']
        long = ville['longitude']

        await interaction.response.defer(ephemeral=True, invisible=False)
        await interaction.followup.delete_message(interaction.message.id)

        paginator = MeteoResult(await _get_embed_from_city(lat, long, ville['name'], ville['country_code'], self.view.complet))
        await paginator.respond(interaction, ephemeral=True)



class MeteoResult(pages.Paginator):
    def __init__(self, pages: list[discord.Embed]):
        super().__init__(
            pages=pages,
            author_check=True,
            use_default_buttons=True
        )




async def _get_embed_from_city(lat: float, long: float, name: str, country_code: str, complet: bool):
    """
    Retourne une liste de discord.Embed qui contiendra les prévisions météo.
    Chaque Embed représente 1 jour, et si l'utilisateur a demandé la précision
    maximale, il contiendra les prévisions heure par heure.
    Sinon, il contiendra les prévisions pour les heures suivantes:
        - 8h
        - 10h
        - 12h
        - 14h
        - 16h
    """
    result: list[discord.Embed] = []
    base_title = f"Météo à `{name}` le "
    desc = ":warning:  *La météo peut ne pas être précise*"
    footer = "Données provenant d'OpenMeteo: https://open-meteo.com/"

    meteo_marine: bool = True
    
    async with aiohttp.ClientSession() as session:
        req = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&hourly=temperature_2m,precipitation_probability,precipitation,windspeed_10m"
        req_marine = f"https://marine-api.open-meteo.com/v1/marine?latitude={lat}&longitude={long}&hourly=wave_height,swell_wave_height&length_unit=metric"

        async with session.get(req) as response:
            ans = await response.json()
        
        async with session.get(req_marine) as response:
            meteo_marine = (response.status) == 200
            ans_marine = await response.json()
    
    desc += f"\n\nPas de données maritime disponible pour {name}" if not meteo_marine else ""


    if complet:
        for i in range(len(ans['hourly']['time'])):
            # Un embed par jour
            if not (i % 24):
                tmp = ans['hourly']['time'][i]
                date_str = f"{tmp[8:10]}/{tmp[5:7]}/{tmp[:4]}"

                new = discord.Embed()
                new.title = base_title + date_str
                new.description = desc
                new.set_footer(text=footer)
                
                result.append(new)
            
            _set_field(result[-1], i, ans, ans_marine, meteo_marine, True)


            
    else:
        for i in range(7):                  # 7 jours de prévision
            tmp = ans['hourly']['time'][i * 24]
            date_str = f"{tmp[8:10]}/{tmp[5:7]}/{tmp[:4]}"

            new = discord.Embed()
            new.title = base_title + date_str
            new.description = desc
            new.set_footer(text=footer)

            for j in range(8, 17, 2):       # 8h, 10h, 12h, 14h et 16h
                _set_field(new, i * 24 + j, ans, ans_marine, meteo_marine, False)

            result.append(new)
        pass

    return result



def _set_field(embed: discord.Embed, i, general_data: dict, marine_data: dict, meteo_marine, complet):
    """
    Remplis l'embed passé en paramètre avec les informations d'indice `i`
    """
    # ans['hourly_units']['temperature_2m'] donne l'unité (ici °C)
    temperature = f":thermometer: {general_data['hourly']['temperature_2m'][i]} {general_data['hourly_units']['temperature_2m']}"
    
    precipitation = "Pas de précipitations"
    if general_data['hourly']['precipitation'][i]:
        precipitation = f":cloud_rain: {general_data['hourly']['precipitation'][i]} {general_data['hourly_units']['precipitation']}"
        precipitation += f" ({general_data['hourly']['precipitation_probability'][i]} %)"
    

    wind_speed = "Pas de vent"
    if general_data['hourly']['windspeed_10m'][i] > 5:
        wind_speed = f":dash: Vent à {general_data['hourly']['windspeed_10m'][i]} {general_data['hourly_units']['windspeed_10m']}"


    wave_height = ""

    if meteo_marine:
        wave_height = f":ocean: Hauteur des vagues: {marine_data['hourly']['wave_height'][i]} {marine_data['hourly_units']['wave_height']}"
        if marine_data['hourly']['swell_wave_height'][i] != marine_data['hourly']['wave_height'][i]:
            wave_height += f" ({marine_data['hourly']['swell_wave_height'][i]} {marine_data['hourly_units']['swell_wave_height']} de houle)"
        
    hour_str = general_data['hourly']['time'][i][11:13] + 'h'
    embed.add_field(
        name = hour_str,
        value='\n'.join([precipitation, temperature, wind_speed, wave_height]),
        inline=complet
    )



def gen_plot(general_data: dict, marine_data: dict):
    """
    Génère le diagramme affichant l'évolution des données sur 7 jours.
    """
    title = hco.Title(text = 'Prévisions sur 7 jours', align = 'center')
    subtitle = hco.Subtitle(text = 'Source: OpenMeteo', align = 'left')

    y_axis = hco.YAxis(title = AxisTitle(text = 'Number of Employees'))

    pass