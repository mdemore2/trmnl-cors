import requests
import json

def query_all():
    query_xkcd()

def query_xkcd():
    url = 'https://xkcd.com/info.0.json'
    resp = requests.get(url)
    data = resp.json()
    with open('data/xkcd.json','w+') as f:
        json.dump(data, f)