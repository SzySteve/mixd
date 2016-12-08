from collections import Counter, defaultdict
from models import Tag, TAG_CATEGORY_GENRE, TAG_CATEGORY_MOOD
from spotipy import Spotify
from spotipy_client import sp_oauth

def get_playlist_genres(tracks, suggestion_count):
    # Pagination should happen, at some point above.
    artists_num_appearances = []
    genres = []

    token = sp_oauth.get_cached_token()['access_token']
    sp = Spotify(token)

    # Assemble a list of all artists represented.
    for track in tracks:
        for artist in track['track']['artists']:
            artists_num_appearances.append(artist['id'])
    # Count it
    artists_num_appearances = Counter(artists_num_appearances)

    # Grab the 10 most common artists in the playlist, and get their genres.
    for artist_id, _ in artists_num_appearances.most_common(10):
        artist_info = sp.artist(artist_id)
        for genre in artist_info['genres']:
            genres.append(genre)
    # Count genres
    genre_counter = Counter(genres)

    top_n_genres = genre_counter.most_common(suggestion_count)

    # Resolve these to actual tag objects
    tags = []
    for genre in top_n_genres:
        name = genre[0]
        tag = Tag.objects.get_or_create(name=name, category=TAG_CATEGORY_GENRE)[0]
        tags.append(tag)
        print tag
    return tags


def average_field(audio_features, feature):
    field_values = [track[feature] for track in audio_features if track[feature] is not None]

    return sum(field_values) / len(field_values)


def suggest_audio_features_tags(tracks):
    tags = []
    token = sp_oauth.get_cached_token()['access_token']
    sp = Spotify(token)
    track_ids = [t['track']['id'] for t in tracks][:min(len(tracks), 100)]
    audio_features = sp.audio_features(tracks=track_ids)

    if average_field(audio_features, 'danceability') > .75:
        tags.append(Tag.objects.get(name="Party", category=TAG_CATEGORY_MOOD))

    avg_tempo = average_field(audio_features, 'tempo')
    if avg_tempo > 120 and avg_tempo < 150:
        tags.append(Tag.objects.get(name="Roadtrip", category=TAG_CATEGORY_MOOD))

    avg_energy = average_field(audio_features, 'energy')
    avg_valence = average_field(audio_features, 'valence')

    # Refactor this bullshit mess
    # No magic numbers
    if avg_energy > .7 and avg_valence > .7:
        tags.append(Tag.objects.get(name="Upbeat", category=TAG_CATEGORY_MOOD))
    elif avg_energy < .4 and avg_valence > .7:
        tags.append(Tag.objects.get(name="Relaxed", category=TAG_CATEGORY_MOOD))
    elif avg_energy < .4 and avg_valence < .4:
        tags.append(Tag.objects.get(name="Melancholy", category=TAG_CATEGORY_MOOD))
    elif avg_energy > .7 and avg_valence < .4:
        tags.append(Tag.objects.get(name="Angry", category=TAG_CATEGORY_MOOD))

    return tags

def suggest_tags(tracks):
    genre_tags = get_playlist_genres(tracks, 10)

    analysis_tags = suggest_audio_features_tags(tracks)
    tags = {
        'genre': genre_tags,
        'mood': analysis_tags
    }

    # Could do a lot more in here. Could parse playlist name and look for keywords, etc.
    # Lot of potential fun.

    return tags
