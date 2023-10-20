from django.forms import ModelForm, TextInput, FileInput, BooleanField
from .models import Track

class TrackForm(ModelForm):
    class Meta:
        model = Track
        fields = ["name", "mp3_file", "minutes", "seconds"]
        class Meta:
            exclude = ('fix_track')
