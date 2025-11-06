import pandas as pd
import random
from itertools import product


def recommend(spotify_df, emotions, situations):
    recommendations = {}
    songs_per_emotion = (20 // len(emotions))

    candidate_songs = spotify_df[(spotify_df['emotion'].isin(emotions)) & (spotify_df[situations].eq(1).any(axis=1))]

    for emotion in emotions:
        for i in range(songs_per_emotion):
            recommendations_df = pd.DataFrame()
            if len(recommendations) == 0:
                situation = random.choice(situations)

            else:
                recommendations_df = pd.concat(list(recommendations.values()), ignore_index=True)
                emotion_subset_df = recommendations_df[recommendations_df['emotion'] == emotion]
                situations_by_count = {}

                for situation in situations:
                    emotion_situation_subset_df = emotion_subset_df[emotion_subset_df[situation] == 1]
                    emotion_situation_count = len(emotion_situation_subset_df)
                    situations_by_count.setdefault(emotion_situation_count, []).append(situation)

                min_situation_count = min(situations_by_count.keys())
                situation = random.choice(situations_by_count[min_situation_count])

            while True:
                sample_song = candidate_songs[(candidate_songs['emotion'] == emotion) & (candidate_songs[situation] == 1)].sample(n=1, ignore_index=True)

                if len(recommendations) == 0:
                    break
                else:
                    duplicate_count = pd.concat([sample_song, recommendations_df]).duplicated().sum()
                    if duplicate_count == 0:
                        break

            recommendations[emotion] = pd.concat([recommendations.get(emotion, pd.DataFrame()), sample_song], axis=0, ignore_index=True)



    missing_count = 20 - (len(emotions) * songs_per_emotion)

    if missing_count > 0:
        combinations = list(product(emotions, situations))

        excluded_emotion = ''
        excluded_situation = ''

        for i in range(missing_count):
            recommendations_df = pd.concat(list(recommendations.values()), ignore_index=True)
            combinations_by_count = {}
            for emotion, situation in combinations:
                emotion_situation_subset_df = recommendations_df[(recommendations_df['emotion'] == emotion) & (recommendations_df[situation] == 1)]
                emotion_situation_count = len(emotion_situation_subset_df)
                combination = (emotion, situation)
                combinations_by_count.setdefault(emotion_situation_count, []).append(combination)

            min_combination_count = min(combinations_by_count.keys())
            while True:
                random_combination = random.choice(combinations_by_count[min_combination_count])
                if ((random_combination[0] != excluded_emotion) & (random_combination[1] != excluded_situation)):
                    break

            excluded_emotion = random_combination[0]
            excluded_situation = random_combination[1]

            while True:
                sample_song = candidate_songs[(candidate_songs['emotion'] == random_combination[0]) & (candidate_songs[random_combination[1]] == 1)].sample(n=1, ignore_index=True)

                if len(recommendations) == 0:
                    break
                else:
                    duplicate_count = pd.concat([sample_song, recommendations_df]).duplicated().sum()
                    if duplicate_count == 0:
                        break

            recommendations[random_combination[0]] = pd.concat([recommendations.get(random_combination[0], pd.DataFrame()), sample_song], axis=0, ignore_index=True)


    final_recommendations = pd.concat(list(recommendations.values()), ignore_index=True)
    return final_recommendations.rename(columns={"song": "title", "ISRC": "isrc"}).to_dict(orient="records")