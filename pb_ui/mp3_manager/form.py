from django.forms import ModelForm, TextInput, FileInput, BooleanField
from django import forms
from .models import Track, Playtime, Playlist, Bridge, Light

class BridgeForm(ModelForm):
    class Meta:
        model = Bridge
        fields = ['ip', 'user_id', 'name_stub', 'brightness']

class LightForm(ModelForm):
    class Meta:
        model = Light
        fields = ['name', 'primary_R', 'primary_G', 'primary_B', 
                  'secondary_R', 'secondary_G', 'secondary_B', 
                  'primary_colour', 'fade', 'random' ]

class TrackForm(ModelForm):
    class Meta:
        model = Track
        fields = ["name", "mp3_file", "minutes", "seconds", "bpm"]

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

class TrackBpmForm(ModelForm):
    bpm = forms.IntegerField(
        label='',
    )
    class Meta:
        model = Track
        fields = ["bpm"]
        exclude = ["name", "mp3_file", "bpm"]


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
