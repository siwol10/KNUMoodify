import pandas as pd
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from recommendation import recommend
from pydantic import BaseModel, Field
from inference import predict_one

@asynccontextmanager
async def load_dataset(app: FastAPI):
    global DF_SPOTIFY
    DF_SPOTIFY = pd.read_json('dataset/spotify_dataset.json', lines=True)

    yield
    DF_SPOTIFY = None

app = FastAPI(lifespan=load_dataset, title="KNU-IEUM", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://localhost:8081"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)

class PredictRequest(BaseModel):
    text: str = Field(..., description="분류할 문장")

class PredictResponse(BaseModel):
    result: str  # 예: emotion="기쁨"

@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    """
    요청:
      { "text": "오늘 기분이 너무 좋아요" }
    응답:
      { "result": "emotion=\"기쁨\"" }
    """
    #return predict_one(req.text)

    emotion = predict_one(req.text)
    return {"result": f'emotion="{emotion}"'}

@app.post("/recommendations")
def analyze_and_recommend(req: PredictRequest):
    emotions = [predict_one(req.text)]
    songs = recommend(DF_SPOTIFY, emotions, ['party', 'work', 'running'])
    return {"songs": songs}