from django import forms

class SearchForm(forms.Form):
    query = forms.CharField(label='Search for a song', max_length=100)

class SongSelectionForm(forms.Form):
    selected_song = forms.ChoiceField(choices=[], widget=forms.RadioSelect)

    def __init__(self, *args, **kwargs):
        choices = kwargs.pop('choices', [])
        super().__init__(*args, **kwargs)
        self.fields['selected_song'].choices = choices
