from django.forms import ModelForm, TextInput, FileInput, BooleanField
from django import forms
from .models import Track, Playtime

class TrackForm(ModelForm):
    class Meta:
        model = Track
        fields = ["name", "mp3_file", "minutes", "seconds"]

class PlaytimeForm(ModelForm):
    class Meta:
        model = Playtime
        fields = ["playtime_seconds", "play_full_override"]

class TrackPlaytimeForm(ModelForm):
    playtime_seconds = forms.IntegerField(
        label='',
    )
    class Meta:
        model = Track
        fields = ["playtime_seconds"]
        exclude = ["name", "mp3_file", "minutes", "seconds"]
