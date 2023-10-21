from django.forms import ModelForm, TextInput, FileInput, BooleanField
from .models import Track, Playtime

class TrackForm(ModelForm):
    class Meta:
        model = Track
        fields = ["name", "mp3_file", "minutes", "seconds"]
        class Meta:
            exclude = ('fix_track')

class PlaytimeForm(ModelForm):
    class Meta:
        model = Playtime
        fields = ["playtime_seconds"]

