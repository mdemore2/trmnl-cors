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
