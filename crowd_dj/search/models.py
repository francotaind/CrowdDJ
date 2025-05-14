from django.db import models

# Create your models here.
# playlist_maker/models.py

from django.db import models

class Playlist(models.Model):
    name = models.CharField(max_length=200)
    spotify_id = models.CharField(max_length=200, blank=True)

class Song(models.Model):
    spotify_id = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name='songs')
