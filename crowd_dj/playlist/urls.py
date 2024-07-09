from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('party/', views.party_room, name='party_room'),
    path('vote/<int:song_id>/', views.vote, name='vote'),
    path('playlist/<int:playlist_id>/play_top_song/', views.play_top_song, name='play_top_song'),
    path('spotify/login/', views.spotify_login, name='spotify_login'),
    path('spotify/callback/', views.spotify_callback, name='spotify_callback'),
    ]
