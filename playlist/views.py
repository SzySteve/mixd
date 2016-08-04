from django.http.response import HttpResponse
from django.shortcuts import render
import json

from models import Playlist, Tag, TAG_CATEGORY_MOOD
from spotipy_client import sp, steve_spotify_id, playlist_id
from suggest_tags import suggest_tags



def seed(request):
    playlists = sp.user_playlists(steve_spotify_id, limit=10)['items']
    for p in playlists:
        print p
        Playlist.objects.create(id=p['id'], user_id=steve_spotify_id, name=p['name'])
    return HttpResponse("seeded with steves playlists")

def tags(request):
    tracks = sp.user_playlist_tracks(steve_spotify_id, playlist_id)['items']
    tags = suggest_tags(tracks)
    return HttpResponse(json.dumps(tags))

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

    return render(request, 'index.html', {'playlists': playlists})

def detail(request):
    id = request.GET['id']
    mixd_playlist = Playlist.objects.get(id=id)

    playlist = sp.user_playlist(user=steve_spotify_id, playlist_id=mixd_playlist.id)
    return render(request, 'playlist.html', {'playlist': playlist,
                                             'description': mixd_playlist.description})
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
    tags = suggest_tags(tracks)
    return render(request, 'tag-and-share.html', {'playlist': playlist,
                                                  'tags': tags})
