from django.forms import ModelForm, TextInput, FileInput
from .models import track

class TrackForm(ModelForm):
    class Meta:
        model = track
        fields = ["name", "mp3_file", "minutes", "seconds"]
        widgets = {
            "name": TextInput(),
            "mp3_file": FileInput(),
            "minutes": TextInput(),
            "seconds": TextInput(),
        }
