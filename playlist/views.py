from django.http.response import HttpResponse
from django.shortcuts import render
import json

from models import Playlist, Tag, TagInstance, TAG_CATEGORY_MOOD, TAG_CATEGORY_GENRE
from spotipy_client import sp, steve_spotify_id, playlist_id
from suggest_tags import suggest_tags


def seedTags(request):
    Tag.objects.create(name="Party", category=TAG_CATEGORY_MOOD)
    Tag.objects.create(name="Upbeat", category=TAG_CATEGORY_MOOD)
    Tag.objects.create(name="Melancholy", category=TAG_CATEGORY_MOOD)
    Tag.objects.create(name="Angry", category=TAG_CATEGORY_MOOD)
    Tag.objects.create(name="Workout", category=TAG_CATEGORY_MOOD)
    Tag.objects.create(name="Relaxed", category=TAG_CATEGORY_MOOD)

def index(request):
    raw_playlists = Playlist.objects.all()
    ids = [p.id for p in raw_playlists]
    playlists = [sp.user_playlist(user=steve_spotify_id, playlist_id=id) for id in ids]

    for playlist in playlists:
        playlist['owner'] = sp.user(playlist['owner']['id'])
        playlist['tags'] = TagInstance.objects.filter(playlist_id=playlist['id'])

    return render(request, 'index.html', {'playlists': playlists})

def detail(request):
    id = request.GET['id']
    mixd_playlist = Playlist.objects.get(id=id)

    playlist = sp.user_playlist(user=steve_spotify_id, playlist_id=mixd_playlist.id)

    tags = TagInstance.objects.filter(playlist=mixd_playlist)

    return render(request, 'playlist.html', {'playlist': playlist,
                                             'description': mixd_playlist.description,
                                             'tags': tags})
def add(request):
    return render(request, 'add.html', {})

def share(request):
    uri = request.POST['uri']
    # ToDo: Gracefully handle errors
    # spotify:user:1210159879:playlist:0v5PyzDU1jZIN7zgvpFfFb
    tokens = uri.split(':')
    user = tokens[2]
    pid = tokens[4]

    playlist = sp.user_playlist(user=user, playlist_id=pid)

    tracks = playlist['tracks']['items']
    suggested_tags = suggest_tags(tracks)

    # messy as shit i dont like this
    all_tags = Tag.objects.all()
    tags = {
        'mood': all_tags.filter(category=TAG_CATEGORY_MOOD),
        'genre': all_tags.filter(category=TAG_CATEGORY_GENRE)
    }

    return render(request, 'tag-and-share.html', {'playlist': playlist,
                                                  'suggested_tags': suggested_tags,
                                                  'tags': tags})

def save(request):
    #Wrap this all in a transaction
    playlist_id = request.POST['playlist_id']
    user_id = request.POST['user_id']
    name = request.POST['name']
    user_tags = json.loads(request.POST['tags'])
    description = request.POST['description']

    mixd_playlist = Playlist.objects.create(id=playlist_id, user_id=user_id,
                                            description=description, name=name)

    # Ensure each tag exists in the DB already
    for category in user_tags.keys():
        tags = user_tags[category]
        for proposed_tag in tags:
            tag = Tag.objects.get_or_create(category=category, name=proposed_tag)[0]
            TagInstance.objects.create(tag=tag, playlist=mixd_playlist)

    return render(request, 'success.html', {'playlist_id': playlist_id})

def search(request):
    return render(request, 'search.html', {})
