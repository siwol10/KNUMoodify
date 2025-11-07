import pandas as pd
import random
from itertools import product


def add_unique_song(emotion, situation, candidate_songs, recommendations):
    while True:
        sample_song = candidate_songs[
            (candidate_songs['emotion'] == emotion) & (candidate_songs[situation] == 1)].sample(n=1, ignore_index=True)

        if len(recommendations) == 0:
            break
        else:
            recommendations_df = pd.concat(list(recommendations.values()), ignore_index=True)
            duplicate_count = pd.concat([sample_song, recommendations_df]).duplicated().sum()
            if duplicate_count == 0:
                break

    recommendations[emotion] = pd.concat([recommendations.get(emotion, pd.DataFrame()), sample_song], axis=0, ignore_index=True)

    return recommendations


def distribute_songs_fairly(emotions, situations, candidate_songs, songs_per_emotion):
    recommendations = {}

    for emotion in emotions:
        for i in (range(songs_per_emotion)):
            if recommendations:
                recommendations_df = pd.concat(list(recommendations.values()), ignore_index=True)
            else:
                recommendations_df = pd.DataFrame(columns=['artist', 'song', 'length', 'emotion', 'ISRC', *situations])

            emotion_subset_df = recommendations_df[recommendations_df['emotion'] == emotion]
            situations_by_count = {}
            for stt in situations:
                if stt in emotion_subset_df.columns:
                    count = int(emotion_subset_df[stt].sum())
                else:
                    count = 0

                situations_by_count.setdefault(count, []).append(stt)

            min_situation_count = min(situations_by_count.keys())
            situation = random.choice(situations_by_count[min_situation_count])

            recommendations = add_unique_song(emotion, situation, candidate_songs, recommendations)

    return recommendations


def distribute_songs_balanced(emotions, situations, candidate_songs, songs_per_emotion):
    recommendations = {}

    for emotion in emotions:
        selected_situations = set()
        for i in (range(songs_per_emotion)):
            if recommendations:
                recommendations_df = pd.concat(list(recommendations.values()), ignore_index=True)
            else:
                recommendations_df = pd.DataFrame(columns=['artist', 'song', 'length', 'emotion', 'ISRC', *situations])

            situations_by_count = {}
            for stt in situations:
                if stt in recommendations_df.columns:
                    count = int(recommendations_df[stt].sum())
                else:
                    count = 0
                situations_by_count.setdefault(count, []).append(stt)

            min_situation_count = min(situations_by_count.keys())
            least_used_situations = situations_by_count[min_situation_count]

            available_situations = []
            for stt in least_used_situations:
                if stt not in selected_situations:
                    available_situations.append(stt)

            if available_situations:
                situation = random.choice(available_situations)
            else:
                situation = random.choice(least_used_situations)
            selected_situations.add(situation)

            recommendations = add_unique_song(emotion, situation, candidate_songs, recommendations)

    return recommendations


def fill_remaining_songs(emotions, situations, missing_count, candidate_songs, recommendations):
    combinations = list(product(emotions, situations))

    excluded_emotion = ''
    excluded_situation = ''

    for i in range(missing_count):
        recommendations_df = pd.concat(list(recommendations.values()), ignore_index=True)
        combinations_by_count = {}
        for emotion, situation in combinations:
            if situation in recommendations_df.columns:
                count = int(recommendations_df[(recommendations_df['emotion'] == emotion) & (recommendations_df[situation] == 1)].shape[0])
            else:
                count = 0

            combination = (emotion, situation)
            combinations_by_count.setdefault(count, []).append(combination)

        min_combination_count = min(combinations_by_count.keys())
        min_combinations = combinations_by_count[min_combination_count]

        filtered_combinations = []
        for cmb in min_combinations:
            if (excluded_emotion not in cmb) & (excluded_situation not in cmb):
                filtered_combinations.append(cmb)


        if filtered_combinations:
            random_combination = random.choice(filtered_combinations)
        else:
            random_combination = random.choice(min_combinations)
        excluded_emotion, excluded_situation = random_combination

        recommendations = add_unique_song(random_combination[0], random_combination[1], candidate_songs, recommendations)

    return recommendations


def recommend(spotify_df, emotions, situations):
    songs_per_emotion = (20 // len(emotions))  # 감정당 곡 수
    candidate_songs = spotify_df[(spotify_df['emotion'].isin(emotions)) & (spotify_df[situations].eq(1).any(axis=1))]

    if songs_per_emotion >= len(situations):
        recommendations = distribute_songs_fairly(emotions, situations, candidate_songs, songs_per_emotion)
    else:
        recommendations = distribute_songs_balanced(emotions, situations, candidate_songs, songs_per_emotion)


    missing_count = 20 - (len(emotions) * songs_per_emotion)
    if missing_count > 0:
        recommendations = fill_remaining_songs(emotions, situations, missing_count, candidate_songs, recommendations)


    if recommendations:
        final_recommendations = pd.concat(list(recommendations.values()), ignore_index=True)
    else:
        final_recommendations = pd.DataFrame(columns=['artist', 'song', 'length', 'emotion', 'ISRC', *situations])


    return final_recommendations.rename(columns={"song": "title", "ISRC": "isrc"}).to_dict(orient="records")