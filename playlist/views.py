from django.shortcuts import render
import json

from models import Playlist, Tag, TagInstance, TAG_CATEGORY_MOOD, TAG_CATEGORY_GENRE
from spotipy_client import sp_oauth
from suggest_tags import suggest_tags
from spotipy import Spotify

def seedTags(request):
    Tag.objects.create(name="Party", category=TAG_CATEGORY_MOOD)
    Tag.objects.create(name="Upbeat", category=TAG_CATEGORY_MOOD)
    Tag.objects.create(name="Melancholy", category=TAG_CATEGORY_MOOD)
    Tag.objects.create(name="Angry", category=TAG_CATEGORY_MOOD)
    Tag.objects.create(name="Workout", category=TAG_CATEGORY_MOOD)
    Tag.objects.create(name="Relaxed", category=TAG_CATEGORY_MOOD)

# List and detail should absolutely be made more DRF-like.
# Pagination will become an necessity once enough Playlists exist.


def get_token(request):
    access_token = None
    token_info = sp_oauth.get_cached_token()
    if token_info:
        access_token = token_info['access_token']
    else:
        url = request.url
        code = sp_oauth.parse_response_code(url)
        if code:
            token_info = sp_oauth.get_access_token(code)
            access_token = token_info['access_token']
    # We should maybe raise here and let individual views take care of it.
    # Realistically though this could maybe become a DRF validation class.
    return access_token


def list(request):
    access_token = get_token(request)

    # Messy but OK for now.
    if not access_token:
        return auth(request)

    sp = Spotify(access_token)

    raw_playlists = Playlist.objects.all()
    playlists = [sp.user_playlist(user=playlist.user_id, playlist_id=playlist.id) for playlist in raw_playlists]

    for playlist in playlists:
        playlist['owner'] = sp.user(playlist['owner']['id'])
        playlist['tags'] = TagInstance.objects.filter(playlist_id=playlist['id'])

    return render(request, 'index.html', {'playlists': playlists})

def detail(request):
    id = request.GET['id']
    mixd_playlist = Playlist.objects.get(id=id)
    access_token = get_token(request)

    sp = Spotify(access_token)
    playlist = sp.user_playlist(user=mixd_playlist.user_id, playlist_id=mixd_playlist.id)

    tags = TagInstance.objects.filter(playlist=mixd_playlist)

    return render(request, 'playlist.html', {'playlist': playlist,
                                             'description': mixd_playlist.description,
                                             'tags': tags})
def add(request):
    return render(request, 'add.html', {})

def auth(request):
    auth_url = sp_oauth.get_authorize_url()
    return render(request, 'auth.html', {'auth_url': auth_url})

def share(request):
    access_token = get_token(request)

    uri = request.POST['uri']
    # ToDo: Gracefully handle errors
    # URI FORMAT: spotify:user:1210159879:playlist:0v5PyzDU1jZIN7zgvpFfFb
    tokens = uri.split(':')
    user = tokens[2]
    pid = tokens[4]

    sp = Spotify(access_token)
    playlist = sp.user_playlist(user=user, playlist_id=pid)

    tracks = playlist['tracks']['items']
    suggested_tags = suggest_tags(tracks)

    # This can possibly be made more efficient...
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
    access_token = get_token(request)

    tag = request.GET['tag']

    raw_playlists = Playlist.objects.filter(tags__name__exact=tag)

    access_token = sp_oauth.get_cached_token()['access_token']
    sp = Spotify(access_token)

    playlists = [sp.user_playlist(user=playlist.user_id, playlist_id=playlist.id) for playlist in raw_playlists]

    for playlist in playlists:
        playlist['owner'] = sp.user(playlist['owner']['id'])
        playlist['tags'] = TagInstance.objects.filter(playlist_id=playlist['id'])

    return render(request, 'index.html', {'playlists': playlists})
