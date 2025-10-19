from fastapi import FastAPI
from query import query_all

app = FastAPI()

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
    pass


@app.get('/surf')
def read_surf():
    pass

@app.get('/refresh')
def refresh_data():
    query_all()
    return "Ahh... refreshing :)"