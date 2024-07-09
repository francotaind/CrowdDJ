import spotipy
from spotipy.oauth2 import SpotifyOAuth
from django.conf import settings
from django.contrib.sessions.backends.db import SessionStore

def search_spotify(spotify_client, query, limit=10):
    try:
        results = spotify_client.search(q=query, type='track', limit=limit)
        tracks = results['tracks']['items']
        return [
            {
                'uri': track['uri'],
                'name': track['name'],
                'artist': track['artists'][0]['name'],
                'album': track['album']['name'],
                'image_url': track['album']['images'][0]['url'] if track['album']['images'] else None
            }
            for track in tracks
        ]
    except Exception as e:
        print(f"Error searching Spotify: {str(e)}")
        return []

def get_spotify_client(request):
    session = SessionStore(session_key=request.session.session_key)
    token_info = session.get('spotify_token_info')

    auth_manager = SpotifyOAuth(
        client_id=settings.SPOTIFY_CLIENT_ID,
        client_secret=settings.SPOTIFY_CLIENT_SECRET,
        redirect_uri=settings.SPOTIFY_REDIRECT_URI,
        scope="user-modify-playback-state user-read-playback-state",
        cache_handler=spotipy.cache_handler.DjangoSessionCacheHandler(request)
    )

    if not token_info:
        # If there's no token, we need to go through the auth flow
        auth_url = auth_manager.get_authorize_url()
        return None, auth_url
    
    spotify_client = spotipy.Spotify(auth_manager=auth_manager)
    return spotify_client, None

def play_song(spotify_client, song_uri):
    try:
        # Get available devices
        devices = spotify_client.devices()
        if not devices['devices']:
            return False, "No active Spotify devices found."
        # Use the first available device
        device_id = devices['devices'][0]['id']
        # Start playback
        spotify_client.start_playback(device_id=device_id, uris=[song_uri])
        return True, "Song started playing successfully."
    except spotipy.exceptions.SpotifyException as e:
        return False, f"Error playing song: {str(e)}"
