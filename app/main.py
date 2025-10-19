from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from query import query_all
import json
import logging

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"]
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
)

@app.get("/")
def read_root():
    return {"Hello":"World"}

@app.get('/news')
def read_news():
    with open('data/news.json', 'r') as f:
        data = json.load(f)
        return data

@app.get('/xkcd')
def read_xkcd():
    with open('data/xkcd.json', 'r') as f:
        data = json.load(f)
        return data
    
@app.get('/wiki')
def read_wiki():
    with open('data/wikipedia.json', 'r') as f:
        data = json.load(f)
        return data

@app.get('/refresh')
def refresh_data():
    query_all()
    return "Ahh... refreshing :)"

@app.get('/surf')
def read_surf():
    pass

@app.get('/wx')
def read_wx():
    pass