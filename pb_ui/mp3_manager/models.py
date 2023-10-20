from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Track(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False)
    mp3_file = models.FileField(upload_to="uploads", blank=False, null=False)
    minutes = models.IntegerField(blank=False, null=False, validators=[MinValueValidator(0),
                                                                       MaxValueValidator(600)])
    seconds = models.IntegerField(blank=False, null=False, validators=[MinValueValidator(0),
                                                                       MaxValueValidator(60)])
    fix_track = models.BooleanField(blank=False, null=False, default=True)

    def __str__(self):
        return self.name

class Playtime(models.Model):
    seconds = models.IntegerField(blank=False, null=False, validators=[MinValueValidator(0),
                                                                       MaxValueValidator(600)])
    def __str__(self):
        return self.play_length
