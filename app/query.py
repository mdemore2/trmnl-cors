import requests
import json
import xml.etree.ElementTree as ET
import logging

logger = logging.getLogger(__name__)

def query_all():
    query_xkcd()
    query_news()

def query_xkcd():
    url = 'https://xkcd.com/info.0.json'
    resp = requests.get(url)
    data = resp.json()
    with open('data/xkcd.json','w+') as f:
        json.dump(data, f)

def query_news():
    #logger.error('TEST')
    url = "https://feeds.npr.org/1001/rss.xml"
    resp = requests.get(url)
    root = ET.fromstring(resp.content)
    channel = root.find('channel')
    logger.error(channel)
    article = channel.find('item')
    logger.error(article)
    for child in article:
        logger.error(child.tag)
    content = article.find('{http://purl.org/rss/1.0/modules/content/}encoded')
    logger.error(content)
    data = {'article': content.text}
    with open('data/news.json', 'w+') as f:
        json.dump(data, f)

