from django import forms
from .models import Song

'''
class songForm(forms.ModelForm):'''

class AddSongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['title', 'artist']

class SongSearchForm(forms.Form):
    query = forms.CharField(label='Search for a song', max_length=100)
