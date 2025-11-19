import pandas as pd
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from recommendation import recommend
from inference import predict_one
from situation_classifier import analyze_situation_list
from schemas import PredictRequest, PredictResponse, WebResponse


@asynccontextmanager
async def load_dataset(app: FastAPI):
    global SPOTIFY_DF
    SPOTIFY_DF = pd.read_json('dataset/spotify_dataset.json', lines=True)

    yield
    SPOTIFY_DF = None

app = FastAPI(lifespan=load_dataset, title="KNU-IEUM", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://localhost:8081"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)

@app.post("/analyze-and-recommend")
def analyze_and_recommend(req: PredictRequest):
    emotions = [predict_one(req.text)]
    situations = analyze_situation_list(req.text)

    if not emotions: # 상황만 입력했을 경우(특정 감정 입력 X) -> 모든 감정을 가지고 플레이리스트 생성
        emotions = ['anger', 'sadness', 'joy', 'surprise', 'fear']

    print('*** input', req)
    print('*** emotions', emotions)
    print('*** situations', situations)

    if 'None' in situations: #목록에 없는 상황이 입력된 경우 선택지 주기
        return WebResponse(selection = True, emotions = emotions, situations = situations, songs = None)
    else: # 목록에 있는 감정/상황이 입력된 경우 추천 진행
        songs = recommend(SPOTIFY_DF, emotions, situations)
        return WebResponse(selection = False, emotions = emotions, situations = situations, songs = songs)

@app.post("/recommend")
def recommend_songs(req: PredictRequest):
    emotions = req.emotions
    situations = req.situations
    songs = recommend(SPOTIFY_DF, emotions, situations)
    return WebResponse(selection = False, emotions = emotions, situations = situations, songs = songs)