from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from query import query_all
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"]
)

@app.get("/")
def read_root():
    return {"Hello":"World"}

@app.get('/wx')
def read_wx():
    pass

@app.get('/news')
def read_news():
    pass

@app.get('/xkcd')
def read_xkcd():
    with open('data/xkcd.json', 'r') as f:
        data = json.load(f)
        return {'img':data['img']}


@app.get('/surf')
def read_surf():
    pass

@app.get('/refresh')
def refresh_data():
    query_all()
    return "Ahh... refreshing :)"