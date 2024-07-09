from django.db import models
from django.contrib.auth.models import User

'''class playlist'''

class Playlist(models.Model):
    """Model definition for Playlist.

    Attributes:
        name: A Charfield to store the name of the playlist.
        created_at: A DateTimeField to store the creation date of the playlist.
        """
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def get_top_voted_song(self):
        """Method to get the top voted song of the playlist."""
        return self.songs.order_by('-votes', '-added_at').first()


    def __str__(self):
        return self.name

'''class song'''

class Song(models.Model):
    """Model definition for Song.

    Attributes:
        title: A Charfield to store the title of the song.
        artist: A Charfield to store the artist of the song.
        playlist: A ForeignKey to store the playlist of the song.
        added_at: A DateTimeField to store the creation date of the song.
        votes: An IntegerField to store the votes of the song.
        added_by: A ForeignKey to store the user who added the song.
        spotify_uri: A Charfield to store the spotify uri of the song.
        """
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE,
            related_name='songs')
    added_at = models.DateTimeField(auto_now_add=True)
    votes = models.IntegerField(default=0)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    spotify_uri = models.CharField(max_length=200)


    def __str__(self):
        return f"{self.title} by {self.artist}"
