from django.shortcuts import render
from django.db import transaction
# Create your views here.
import requests
from django.shortcuts import render, redirect
from django.conf import settings
from .forms import SearchForm, SongSelectionForm
from .models import Playlist, Song

def search_song(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            
            # Get Spotify access token
            auth_response = requests.post('https://accounts.spotify.com/api/token', {
                'grant_type': 'client_credentials',
                'client_id': settings.SPOTIFY_CLIENT_ID,
                'client_secret': settings.SPOTIFY_CLIENT_SECRET,
            })
            access_token = auth_response.json()['access_token']

            # Search for tracks
            headers = {'Authorization': f'Bearer {access_token}'}
            search_response = requests.get(f'https://api.spotify.com/v1/search?q={query}&type=track&limit=5', headers=headers)
            results = search_response.json()['tracks']['items']

            choices = [(track['id'], f"{track['name']} - {track['artists'][0]['name']}") for track in results]
            selection_form = SongSelectionForm(choices=choices)

            return render(request, 'search/search_results.html', {'form': selection_form})
    else:
        form = SearchForm()
    
    return render(request, 'search/search_song.html', {'form': form})

def add_to_playlist(request):
    if request.method == 'POST':
        form = SongSelectionForm(request.POST, choices=[])
        if form.is_valid():
            selected_song_id = form.cleaned_data['selected_song']
            
            # Get Spotify access token
            auth_response = requests.post('https://accounts.spotify.com/api/token', {
                'grant_type': 'client_credentials',
                'client_id': settings.SPOTIFY_CLIENT_ID,
                'client_secret': settings.SPOTIFY_CLIENT_SECRET,
            })
            access_token = auth_response.json()['access_token']

            # Get track details
            headers = {'Authorization': f'Bearer {access_token}'}
            track_response = requests.get(f'https://api.spotify.com/v1/tracks/{selected_song_id}', headers=headers)
            track = track_response.json()

            print(f"Track details: {track}")  # Debug print

            # Add song to the playlist
            try:
                with transaction.atomic():
                    playlist, created = Playlist.objects.get_or_create(name='My Playlist')
                    song = Song.objects.create(
                        spotify_id=track['id'],
                        name=track['name'],
                        artist=track['artists'][0]['name'],
                        playlist=playlist
                    )
                    print(f"Song added to playlist: {song.name} - {song.artist} (ID: {song.id})")  # Debug print
            except Exception as e:
                print(f"Error adding song to playlist: {str(e)}")  # Debug print
                # You might want to add some error handling here

            # Verify the song was saved
            saved_song = Song.objects.filter(spotify_id=track['id']).first()
            if saved_song:
                print(f"Song found in database: {saved_song.name} - {saved_song.artist} (ID: {saved_song.id})")
            else:
                print("Song not found in database after saving")

            return redirect('view_playlist')

    return redirect('search_song')

def view_playlist(request):
    playlist = Playlist.objects.first()
    if playlist:
        print(f"Playlist found: {playlist.name} (ID: {playlist.id})")
        songs = Song.objects.filter(playlist=playlist)
        print(f"Number of songs in playlist: {songs.count()}")
        for song in songs:
            print(f"Song in playlist: {song.name} - {song.artist} (ID: {song.id})")
    else:
        print("No playlist found")
        songs = []
    return render(request, 'search/view_playlist.html', {'songs': songs})
