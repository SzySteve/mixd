from spotipy import oauth2

# janglin playlist, for testing
playlist_id = "0kVeqRxyuGuVqBE6LMjoOq"

sp_credentials = oauth2.SpotifyClientCredentials()

sp_oauth = oauth2.SpotifyOAuth(sp_credentials.client_id,
                               sp_credentials.client_secret,
                               redirect_uri='http://www.szysteve.com/mixd/list',
                               scope='playlist-modify-public',
                               cache_path='.spotipyoauthcache')
