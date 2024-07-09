from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Playlist, Song
from .forms import AddSongForm, SongSearchForm
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .spotify_utils import get_spotify_client, play_song, search_spotify
from django.shortcuts import redirect
from spotipy.oauth2 import SpotifyOAuth
from django.conf import settings


# Create your views here.

def index(request):
    return render(request, 'playlist/index.html')

@login_required
def play_top_song(request, playlist_id):
    playlist = get_object_or_404(Playlist, id=playlist_id)
    top_song = playlist.get_top_voted_song()

    if not top_song:
        messages.warning(request, "No songs in the playlist.")
        return redirect('party_room')

    spotify_client = get_spotify_client()
    success, message = play_song(spotify_client, top_song.spotify_uri)

    if success:
        messages.success(request, f"Now playing: {top_song.title} by {top_song.artist}")
    else:
        messages.error(request, message)

    return redirect('party_room')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            messages.success(request, f'Account created for {username}!')
            return redirect('party_room')  # or wherever you want to redirect after registration
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def party_room(request):
    playlist, created = Playlist.objects.get_or_create(name="Main Playlist")
    songs = playlist.songs.all().order_by('-votes', '-added_at')
    add_song_form = AddSongForm()
    search_form = SongSearchForm()
    search_results = []

    if request.method == 'POST':
        if 'search' in request.POST:
            search_form = SongSearchForm(request.POST)
            if search_form.is_valid():
                query = search_form.cleaned_data['query']
                spotify_client = get_spotify_client(request)
                search_results = search_spotify(spotify_client, query)
        elif 'add_from_search' in request.POST:
            uri = request.POST.get('uri')
            name = request.POST.get('name')
            artist = request.POST.get('artist')
            if uri and name and artist:
                Song.objects.create(
                    playlist=playlist,
                    spotify_uri=uri,
                    title=name,
                    artist=artist,
                    added_by=request.user
                )
                messages.success(request, f'Added "{name}" by {artist} to the playlist.')
            return redirect('party_room')
        else:
            add_song_form = AddSongForm(request.POST)
            if add_song_form.is_valid():
                song = add_song_form.save(commit=False)
                song.playlist = playlist
                song.added_by = request.user
                song.save()
                return redirect('party_room')

    context = {
        'playlist': playlist,
        'songs': songs,
        'add_song_form': add_song_form,
        'search_form': search_form,
        'search_results': search_results,
    }
    return render(request, 'playlist/party_room.html', context)



@login_required
def vote(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    vote_type = request.POST.get('vote_type')
    
    if vote_type == 'up':
        song.votes += 1
    elif vote_type == 'down':
        song.votes -= 1
    
    song.save()
    return redirect('party_room')

def spotify_login(request):
    sp_oauth = SpotifyOAuth(
        client_id=settings.SPOTIFY_CLIENT_ID,
        client_secret=settings.SPOTIFY_CLIENT_SECRET,
        redirect_uri=settings.SPOTIFY_REDIRECT_URI,
        scope="user-modify-playback-state user-read-playback-state"
    )
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

def spotify_callback(request):
    sp_oauth = SpotifyOAuth(
        client_id=settings.SPOTIFY_CLIENT_ID,
        client_secret=settings.SPOTIFY_CLIENT_SECRET,
        redirect_uri=settings.SPOTIFY_REDIRECT_URI,
        scope="user-modify-playback-state user-read-playback-state"
    )
    code = request.GET.get('code')
    token_info = sp_oauth.get_access_token(code)
    request.session['spotify_token_info'] = token_info
    return redirect('party_room')

