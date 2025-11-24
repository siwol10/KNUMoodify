import pandas as pd
from contextlib import asynccontextmanager
import spotipy
from spotipy.exceptions import SpotifyException
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, HTMLResponse
from recommendation import recommend, sp_oauth
from inference import predict_one
from situation_classifier_openai import classify_situation_kor
from schemas import Request, Response, PlaylistRequest, LoginResponse
from typing import Dict
from uuid import uuid4

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

STATE_STORE: Dict[str, Dict] = {}

@app.post("/analyze-and-recommend", response_model=Response)
def analyze_and_recommend(req: Request):
    ALL_EMOTIONS =['anger', 'sadness', 'joy', 'surprise', 'fear']
    emotions = [predict_one(req.text)]

    #openAI 기반 상황 분류로 교체
    raw_situations = classify_situation_kor(req.text)

    # 3) 상황 리스트 후처리
    #    - 상황 단서 없음: ['None']
    #    - 확정 1개: ['situation']
    #    - 모호한 경우(2개 이상): 상위 2개 ['situation1', 'situation2']
    if not raw_situations:
        situations = ['None']
    elif len(raw_situations) == 1:
        situations = raw_situations
    else:
        situations = raw_situations[:2]

    print('*** input: ', req)
    print('*** situations: ', situations)
    print('*** emotions: ', emotions)
    print('*** choice: ', req.choice)

    if not emotions: # 상황만 입력했을 경우(특정 감정 입력 X) -> 모든 감정을 가지고 플레이리스트 생성
        emotions = ALL_EMOTIONS

    if set(emotions) != set(ALL_EMOTIONS) and req.choice == 'Y': # 감정 해소용 매핑
        emotion_mapping = {'anger': 'sadness', 'sadness': 'joy', 'fear': 'joy', 'surprise': 'joy', 'joy': 'joy'}
        emotions = [emotion_mapping[emotions[0]]]
        print('*** emotion mapping: ', emotions)

    print('*** 최종 emotion: ', emotions)

    if 'None' in situations: #목록에 없는 상황이 입력된 경우 선택지 주기
        return Response(selection = True, emotions = emotions, situations = situations, songs = None)
    else: # 목록에 있는 감정/상황이 입력된 경우 추천 진행
        songs = recommend(SPOTIFY_DF, emotions, situations)
        return Response(selection = False, emotions = emotions, situations = situations, songs = songs)

@app.post("/recommend", response_model=Response)
def recommend_songs(req: Request):
    emotions = req.emotions
    situations = req.situations

    songs = recommend(SPOTIFY_DF, emotions, situations)
    return Response(selection = False, emotions = emotions, situations = situations, songs = songs)

@app.post("/spotify-login", response_model=LoginResponse)
def start_spotify_login(req: PlaylistRequest):
    if not req.track_ids:
        raise HTTPException(status_code=400, detail="track_ids가 비어 있습니다.")

    state = uuid4().hex

    STATE_STORE[state] = {
        "track_ids": req.track_ids,
        "name": req.name
    }

    authorize_url = sp_oauth.get_authorize_url(state=state)

    return LoginResponse(authorize_url=authorize_url)

@app.get("/callback")
def spotify_callback(code: str | None = None, state: str | None = None):
    if code is None or state is None:
        raise HTTPException(status_code=400, detail="code 또는 state가 없습니다.")

    if state not in STATE_STORE:
        raise HTTPException(status_code=400, detail="유효하지 않은 state 입니다.")

    data = STATE_STORE.pop(state)
    track_ids = data["track_ids"]
    playlist_name = data["name"]

    token_info = sp_oauth.get_access_token(code, check_cache=False)
    access_token = token_info["access_token"]
    sp_user = spotipy.Spotify(auth=access_token)

    try:
        user = sp_user.current_user()
    except SpotifyException as e: # 대시보드에 등록 안 된 계정 -> alert 창 띄우기
        if e.http_status == 403 and "user may not be registered" in str(e):
            html = """
            <html>
              <body>
                <script>
                  alert('Spotify API 개발 모드 제한으로 인해 등록된 계정만 플레이리스트 저장이 가능합니다.');
                  window.close();
                </script>
              </body>
            </html>
             """
            return HTMLResponse(content=html, status_code=200)
        raise

    user_id = user["id"]

    playlist = sp_user.user_playlist_create(
        user=user_id,
        name=playlist_name,
        public=False,
        description=""
    )

    playlist_id = playlist["id"]

    if track_ids:
        sp_user.playlist_add_items(playlist_id, track_ids)

    sp_user.playlist_change_details(
        playlist_id=playlist_id,
        public=False,
        description=""
    )

    playlist_fetched = sp_user.playlist(playlist_id)

    playlist_url = playlist_fetched["external_urls"]["spotify"]

    return RedirectResponse(url=playlist_url)