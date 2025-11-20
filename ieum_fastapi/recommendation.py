import pandas as pd
import random
from itertools import product
from settings import settings
import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
from spotipy.exceptions import SpotifyException

"""

<추천 과정>
1. 스포티파이 데이터셋에서 조건에 맞는 18~20곡 추출
2. 각 곡의 가수+제목으로 스포티파이 검색 (Spotify API)
    - 올바른 검색 결과가 나오면: 해당 곡의 ID 및 해당 곡으로 연결되는 url 저장
    - 올바르지 않은 검색 결과(검색 결과가 없거나 데이터셋의 정보랑 일치하지 않는 노래)가 나오면: 해당 노래 제외
3. 모자란 곡 수 채우기
    - 이때는 한 곡을 추출할 때마다 Spotify API를 통한 검색 진행 (위와 같이 올바르지 않은 검색 결과가 나오면 해당 노래 제외 후 다시 곡 추출 진행)

* 곡을 추출할 때(1, 3)는 상황 및 감정의 비율이 균등하게 나타나도록 추출 + 중복 검사 진행

"""

sp_oauth = SpotifyOAuth(
    client_id=settings.SPOTIFY_CLIENT_ID,
    client_secret=settings.SPOTIFY_CLIENT_SECRET,
    redirect_uri=settings.SPOTIFY_REDIRECT_URI,
    scope='playlist-modify-private playlist-modify-public'
)

sp_search = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(
        client_id=settings.SPOTIFY_CLIENT_ID,
        client_secret=settings.SPOTIFY_CLIENT_SECRET
    )
)



# 가수 이름 + 노래 제목으로 중복 체크
def is_duplicate_song(sample_song, recommendations):
    if not recommendations:
        return False

    recommendations_df = pd.concat(list(recommendations.values()), ignore_index=True)

    sample_song_artist = str(sample_song["artist"].iloc[0]).strip().lower()
    sample_song_title = str(sample_song["song"].iloc[0]).strip().lower()

    is_duplicate = (recommendations_df["artist"].astype(str).str.strip().str.lower().eq(sample_song_artist) & recommendations_df["song"].astype(str).str.strip().str.lower().eq(sample_song_title)).any()

    return is_duplicate




# 랜덤으로 곡 추출, 중복 검사
def add_unique_song(emotion, situation, candidate_songs, recommendations):
    for i in range(30): # 반복 최대 30번 진행
        sample_song = candidate_songs[(candidate_songs['emotion'] == emotion) & (candidate_songs[situation] == 1)].sample(n=1, ignore_index=True) # 랜덤으로 곡 추출

        if is_duplicate_song(sample_song, recommendations): # 중복 체크
            continue

        recommendations[emotion] = pd.concat([recommendations.get(emotion, pd.DataFrame()), sample_song], axis=0, ignore_index=True) # 중복 아니면 해당 곡 저장

        return recommendations

    # 30번 반복해도 중복 아닌 곡이 없을 때는 넘어감
    return recommendations




# 감정 및 상황의 비율이 균등하게 나타나도록 추출
def generate_initial_recommendations(emotions, situations, candidate_songs, songs_per_emotion):
    recommendations = {}

    for emotion in emotions:
        for i in (range(songs_per_emotion)):
            if recommendations:
                recommendations_df = pd.concat(list(recommendations.values()), ignore_index=True)
            else:
                recommendations_df = pd.DataFrame(columns=['artist', 'song', 'length', 'emotion', 'ISRC', *situations])

            # 해당 감정에서의 상황 빈도수 카운트
            emotion_subset_df = recommendations_df[recommendations_df['emotion'] == emotion]
            situations_by_count = {}
            for stt in situations:
                if stt in emotion_subset_df.columns:
                    count = int(emotion_subset_df[stt].sum())
                else:
                    count = 0

                situations_by_count.setdefault(count, []).append(stt)

            # 가장 적은 빈도수의 상황 중 하나 선택
            min_situation_count = min(situations_by_count.keys())
            situation = random.choice(situations_by_count[min_situation_count])

            # 해당 감정 + 상황 조합으로 랜덤 추출 진행
            recommendations = add_unique_song(emotion, situation, candidate_songs, recommendations)

    return recommendations




# 각 곡의 가수+제목으로 스포티파이 검색 (Spotify API)
def update_tracks_in_recommendations(recommendations):
    for emotion, df in recommendations.items():
        drop_index = [] # 제외할 노래 인덱스 저장

        for idx, row in df.iterrows():
            artist = str(row['artist']).strip()
            song = str(row['song']).strip()

            query = f"{artist} {song}"
            try:
                results = sp_search.search(q=query, type="track", limit=1)
            except Exception: # 검색 에러나면 해당 노래 제외
                drop_index.append(idx)
                continue

            items = results.get("tracks", {}).get("items", [])

            if not items: # 검색 결과가 없으면 해당 노래 제외
                drop_index.append(idx)
                continue

            # 검색 결과가 있으면
            track = items[0]
            track_id = track["id"]
            track_url = track["external_urls"]["spotify"]
            track_name = track["name"]
            artists = ",".join(a["name"] for a in track["artists"])

            dataset_artists = [a.strip().lower() for a in artist.split(",")] # 데이터셋에 있는 가수 정보
            spotify_artists = [a.strip().lower() for a in artists.split(",")] # 스포티파이 검색 결과로 나온 가수 정보

            artists_match = any(a in spotify_artists for a in dataset_artists) # 데이터셋의 가수 정보와 스포티파이 검색 결과로 나온 가수 정보가 일치하는지
            title_match = song.lower() in track_name.lower() # 데이터셋의 제목과 스포티파이 검색 결과로 나온 제목이 일치하는지

            if not (artists_match and title_match): # 데이터셋의 정보와 스포티파이 검색 결과가 일치하지 않으면 제외
                drop_index.append(idx)
                continue

            # 데이터셋의 정보와 스포티파이 검색 결과가 일치하면 해당 곡의 ID 및 해당 곡으로 연결되는 url 저장
            df.at[idx, 'track_id'] = track_id
            df.at[idx, 'track_url'] = track_url

        recommendations[emotion] = df.drop(drop_index)

    return recommendations




# 모자란 곡 수 채우기
def fill_remaining_songs(emotions, situations, missing_count, candidate_songs, recommendations):
    for i in range(missing_count):
        recommendations_df = pd.concat(list(recommendations.values()), ignore_index=True)

        # 감정별 곡 수 카운트
        emotions_by_count = {}
        for emt in emotions:
            emotion_subset_df = recommendations_df[recommendations_df['emotion'] == emt]
            count = len(emotion_subset_df)
            emotions_by_count.setdefault(count, []).append(emt)

        # 가장 적은 빈도수의 감정 중 하나 선택
        min_emotion_count = min(emotions_by_count.keys())
        emotion = random.choice(emotions_by_count[min_emotion_count])

        # 선택된 감정에서의 상황 빈도수 카운트
        emotion_subset_df = recommendations_df[recommendations_df['emotion'] == emotion]
        situations_by_count = {}
        for stt in situations:
            if stt in emotion_subset_df.columns:
                count = int(emotion_subset_df[stt].sum())
            else:
                count = 0

            situations_by_count.setdefault(count, []).append(stt)

        # 가장 적은 빈도수의 상황 중 하나 선택
        min_situation_count = min(situations_by_count.keys())
        situation = random.choice(situations_by_count[min_situation_count])

        subset_df = candidate_songs[(candidate_songs['emotion'] == emotion) & (candidate_songs[situation] == 1)]  # 선택된 감정, 상황 조합의 곡들 추출

        if subset_df.empty:
            break

        found = False

        for j in range(30):  # 반복 최대 30번 진행
            sample_song = subset_df.sample(n=1, ignore_index=True) # 랜덤 선택

            artist = sample_song['artist'].iloc[0]
            song = sample_song['song'].iloc[0]

            artist = str(artist).strip()
            song = str(song).strip()

            # 검색 진행 (Spotify API)
            query = f"{artist} {song}"
            try:
                results = sp_search.search(q=query, type="track", limit=1)
            except Exception: # 검색 에러나면 곡 랜덤 추출 다시 진행
                continue

            items = results.get("tracks", {}).get("items", [])

            if not items: # 검색 결과가 없으면 곡 랜덤 추출 다시 진행
                continue

            # 검색 결과가 있으면
            track = items[0]
            track_id = track["id"]
            track_url = track["external_urls"]["spotify"]
            track_name = track["name"]
            artists = ",".join(a["name"] for a in track["artists"])

            dataset_artists = [a.strip().lower() for a in artist.split(",")] # 데이터셋에 있는 가수 정보
            spotify_artists = [a.strip().lower() for a in artists.split(",")] # 스포티파이 검색 결과로 나온 가수 정보

            artist_match = any(a in spotify_artists for a in dataset_artists) # 데이터셋의 가수 정보와 스포티파이 검색 결과로 나온 가수 정보가 일치하는지
            title_match = song.lower() in track_name.lower() # 데이터셋의 제목과 스포티파이 검색 결과로 나온 제목이 일치하는지

            if not (artist_match and title_match): # 데이터셋의 정보와 스포티파이 검색 결과가 일치하지 않으면 곡 랜덤 추출 다시 진행
                continue

            if is_duplicate_song(sample_song, recommendations): # 중복 체크
                continue

            # 데이터셋의 정보와 스포티파이 검색 결과가 일치하면 해당 곡의 ID 및 해당 곡으로 연결되는 url 저장
            sample_song["track_id"] = track_id
            sample_song["track_url"] = track_url

            recommendations[emotion] = pd.concat([recommendations.get(emotion, pd.DataFrame()), sample_song], axis=0, ignore_index=True)

            found = True
            break

        if not found:
            print("해당 조합 곡 X")

    return recommendations




def recommend(spotify_df, emotions, situations):
    songs_per_emotion = (20 // len(emotions))  # 감정당 곡 수
    candidate_songs = spotify_df[(spotify_df['emotion'].isin(emotions)) & (spotify_df[situations].eq(1).any(axis=1))] # 후보곡

    recommendations = generate_initial_recommendations(emotions, situations, candidate_songs, songs_per_emotion) # 감정 및 상황 비율 균등하게 20곡 추출
    recommendations = update_tracks_in_recommendations(recommendations) # Spotify API로 검색

    total = sum(len(df) for df in recommendations.values())
    missing_count = 20 - total
    if missing_count > 0:
        recommendations = fill_remaining_songs(emotions, situations, missing_count, candidate_songs, recommendations) # 모자란 곡 수 채우기

    final_recommendations = pd.concat(list(recommendations.values()), ignore_index=True)
    final_recommendations = final_recommendations.sample(frac=1).reset_index(drop=True)

    return final_recommendations.rename(columns={"song": "title", "ISRC": "isrc", "track_id": "id", "track_url": "url"}).to_dict(orient="records")