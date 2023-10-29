from django.forms import ModelForm, TextInput, FileInput, BooleanField
from django import forms
from .models import Track, Playtime, Playlist

class TrackForm(ModelForm):
    class Meta:
        model = Track
        fields = ["name", "mp3_file", "minutes", "seconds"]

class PlaytimeForm(ModelForm):
    class Meta:
        model = Playtime
        fields = ["playtime_seconds", "play_full_override", "play_whole_playlist"]

class TrackPlaytimeForm(ModelForm):
    playtime_seconds = forms.IntegerField(
        label='',
    )
    class Meta:
        model = Track
        fields = ["playtime_seconds"]
        exclude = ["name", "mp3_file", "minutes", "seconds"]

class TrackStartForm(ModelForm):
    class Meta:
        model = Track
        fields = [ "minutes", "seconds"]

class PlaylistForm(ModelForm):
    class Meta:
        model = Playlist
        fields = ["name", ]

class PlayDeleteForm(ModelForm):
    class Meta:
        model = Playlist
        fields = ["name", ]
