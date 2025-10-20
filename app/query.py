import requests
import json
import xml.etree.ElementTree as ET
import logging
from datetime import datetime
from dotenv import load_dotenv
import os

logger = logging.getLogger(__name__)
load_dotenv()

def query_all():
    query_xkcd()
    query_news()
    query_wikipedia()
    query_weather()
    query_surfline()

def query_xkcd():
    url = 'https://xkcd.com/info.0.json'
    resp = requests.get(url)
    data = resp.json()
    with open('data/xkcd.json','w+') as f:
        json.dump(data, f)

def query_news():
    url = "https://feeds.npr.org/1001/rss.xml"
    resp = requests.get(url)
    root = ET.fromstring(resp.content)
    channel = root.find('channel')
    article = channel.find('item')
    content = article.find('{http://purl.org/rss/1.0/modules/content/}encoded')
    data = {'article': content.text}
    with open('data/news.json', 'w+') as f:
        json.dump(data, f)

def query_wikipedia():
    today = datetime.now()
    token = os.getenv('WIKI_API_TOKEN')
    app_name = os.getenv('WIKI_API_APP_NAME')
    url = f"https://api.wikimedia.org/feed/v1/wikipedia/en/featured/{today.year}/{today.month}/{today.day}"
    headers = {
      'Authorization': f'Bearer {token}',
      'User-Agent': f'{app_name}'
    }
    resp = requests.get(url, headers=headers)
    logger.info(url)
    logger.info(resp)
    data = resp.json()
    with open('data/wikipedia.json', 'w+') as f:
        json.dump(data,f)


def query_weather():
    wx_key = os.getenv('WEATHER_API_KEY')
    zip_code = os.getenv('WEATHER_ZIP_CODE')
    url = f"http://api.weatherapi.com/v1/forecast.json?key={wx_key}&q={zip_code}&days=2&aqi=no&alerts=no"
    resp = requests.get(url)
    data = resp.json()
    with open('data/weather.json','w+') as f:
        json.dump(data,f)


def query_surfline():
    # conditions BLUF: para
    #surf height: min-max ft
    #conditions rating: x/5 'fair'
    #tides: normal / low/high
    # water temp: *F

    #Surfline Ratings
    #Very Poor: 1 bar
    #Poor: 2 bars
    #Poor to Fair: 3 bars
    #Fair: 4 bars
    #Fair to Good: 5 bars

    spot_id = os.getenv('SURFLINE_SPOT_ID')
    buoy_id = os.getenv('SURFLINE_BUOY_ID')
    surf_dict = {}

    #index 0 returned = midnight
    time_index = datetime.now().hour

    conditionUrl = f"https://services.surfline.com/kbyg/regions/forecasts/conditions?spotId={spot_id}&days=1"
    resp = requests.get(conditionUrl)
    data = resp.json()
    surf_dict['condition'] = data['data']['conditions'][0]['headline']

    wavesUrl = f"https://services.surfline.com/kbyg/spots/forecasts/surf?spotId={spot_id}&units[waveHeight]=FT&days=1"
    resp = requests.get(wavesUrl)
    data = resp.json()
    surf_dict['waves_min'] = data['data']['surf'][time_index]['surf']['min']
    surf_dict['waves_max'] = data['data']['surf'][time_index]['surf']['max']
    surf_dict['waves_desc'] = data['data']['surf'][time_index]['surf']['humanRelation']

    ratingUrl = f"https://services.surfline.com/kbyg/spots/forecasts/rating?spotId={spot_id}&days=1"
    resp = requests.get(ratingUrl)
    data = resp.json()
    surf_dict['rating_num'] = data['data']['rating'][time_index]['rating']['value']
    surf_dict['rating_desc'] = data['data']['rating'][time_index]['rating']['key']

    windUrl = f"https://services.surfline.com/kbyg/spots/forecasts/wind?spotId={spot_id}&days=1&units%5BwindSpeed%5D=KTS"
    resp = requests.get(windUrl)
    data = resp.json()
    surf_dict['wind_speed'] = data['data']['wind'][time_index]['speed']
    surf_dict['wind_dir'] = data['data']['wind'][time_index]['directionType']

    tidesUrl = f"https://services.surfline.com/kbyg/spots/forecasts/tides?spotId={spot_id}&days=1&units%5BtideHeight%5D=FT"
    resp = requests.get(tidesUrl)
    data = resp.json()
    surf_dict['tide_state'] = data['data']['tides'][time_index]['type']
    surf_dict['tide_ht'] = data['data']['tides'][time_index]['height']

    #weatherUrl = f"https://services.surfline.com/kbyg/spots/forecasts/weather?spotId={spot_id}&days=1&units%5Btemperature%5D=F"
    buoyUrl = f"https://services.surfline.com/kbyg/buoys/report/{buoy_id}?days=1"
    resp = requests.get(buoyUrl)
    data = resp.json()
    surf_dict['water_temp'] = data['data'][0]['waterTemperature'] #buoy endpoint returns most recent first

    with open('data/surf.json','w+') as f:
        json.dump(surf_dict,f)



