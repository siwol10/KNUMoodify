import pandas as pd
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from recommendation import recommend

@asynccontextmanager
async def load_dataset(app: FastAPI):
    global DF_SPOTIFY
    DF_SPOTIFY = pd.read_json('dataset/spotify_dataset.json', lines=True)

    yield
    DF_SPOTIFY = None

app = FastAPI(lifespan=load_dataset)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://localhost:8081"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)

@app.post("/recommendations")
def create_recommendations():
    songs = recommend(DF_SPOTIFY, ['anger', 'sadness', 'fear'], ['party', 'work', 'running'])
    return {"songs": songs}