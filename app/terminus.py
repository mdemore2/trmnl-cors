import os
import logging
import requests
import json
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List
from bs4 import BeautifulSoup

load_dotenv()
terminus_url = os.getenv('TERMINUS_URL')
terminus_port = os.getenv('TERMINUS_PORT')
terminus_base_url = f'http://{terminus_url}:{terminus_port}'

logger = logging.getLogger(__name__)

SCREEN_PREFIX = 'TRMNL_CORS'
PLAYLIST_ID = '9'

class Playlist(BaseModel):
    id: int
    screens: List[int]


def add_screen(name: str, content: str, model_id:int) -> int:
    prefixed_name = f'{SCREEN_PREFIX}-{name}'
    data = {'screen':{
        'label':prefixed_name,
        'content':content,
        'name':prefixed_name,
        'file_name':f'{prefixed_name}.png',
        'model_id': str(model_id)
    }}
    headers = {'Content-Type': 'application/json'}
    resp = requests.post(url=f'{terminus_base_url}/api/screens', headers=headers, json=data)
    screen = resp.json()
    return screen['data']['id']

def delete_screen(id:int) -> bool:
    resp = requests.delete(url=f'{terminus_base_url}/api/screens/{str(id)}')
    return resp.ok

def get_screens() -> json:
    resp = requests.get(url=f'{terminus_base_url}/api/screens')
    screens = resp.json()
    return screens['data']

def delete_my_screens():
    screens = get_screens()
    for screen in screens:
        if str(screen['name']).startswith(SCREEN_PREFIX):
            delete_screen(screen['id'])

def create_my_screens():
    pass

def add_to_playlist(screen_id:int):
    #NEED CSRF TOKEN AND COOKIE

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {'playlist_item[screen_id]': str(screen_id)}

    with requests.Session() as s:
        #Get Terminus session cookie
        resp = s.get(url=f'{terminus_base_url}/playlists/{PLAYLIST_ID}/items/new')

        #Parse out csrf token
        soup = BeautifulSoup(resp.text, 'lxml')
        csrf_token = soup.find('input',attrs = {'name':'_csrf_token'})['value']
        payload['_csrf_token'] = csrf_token

        #Post the screen
        resp = s.post(url=f'{terminus_base_url}/playlists/{PLAYLIST_ID}/items', headers=headers, data=payload)
    return resp.ok



def reload():
    delete_my_screens()
    pass
    #get screens
    #ITERATE over screens:
        #delete screens with prefix
    #ITERATE over template files:
        #create screen
        #add screen to playlist


if __name__ == "__main__":
    with open ('templates/news.html', 'r') as f:
        content = f.read()
    #add_screen('pytest',content, 1)
    #get_screens()
    add_to_playlist(131)
    

