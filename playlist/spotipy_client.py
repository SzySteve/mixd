import spotipy
from spotipy.util import prompt_for_user_token

# janglin playlist, for testing
playlist_id = "0kVeqRxyuGuVqBE6LMjoOq"

steve_spotify_id = '1210159879'

trevor_spotify_id = "123004043"

token = prompt_for_user_token(steve_spotify_id, 'playlist-modify-public')

sp = spotipy.Spotify(token)
