from django.shortcuts import render
# from django.template import loader
from django.http.response import HttpResponse
from models import Playlist, Tag, TAG_CATEGORY_MOOD
from spotipy_client import sp, steve_spotify_id, playlist_id
from suggest_tags import suggest_tags
import json

# Create your views here.
# def index(request):
#     playlists = Playlist.objects.all()
#     return HttpResponse(str([p.spotify_id for p in playlists]))

def seed(request):
    playlists = sp.user_playlists(steve_spotify_id, limit=10)['items']
    for p in playlists:
        print p
        Playlist.objects.create(spotify_id=p['id'], user_id=steve_spotify_id, name=p['name'])
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
    pids = [p.spotify_id for p in raw_playlists]
    ids = [p.id for p in raw_playlists]
    playlists = [sp.user_playlist(user=steve_spotify_id, playlist_id=pid) for pid in pids]

    for playlist, id in zip(playlists, ids):
        playlist['mixd_id'] = id

    return render(request, 'index.html', {'playlists': playlists})

def detail(request):
    mixd_id = request.GET['id']
    mixd_playlist = Playlist.objects.get(id=mixd_id)

    playlist = sp.user_playlist(user=steve_spotify_id, playlist_id=mixd_playlist.spotify_id)
    return render(request, 'playlist.html', {'playlist': playlist,
                                             'description': mixd_playlist.description})
