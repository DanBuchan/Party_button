from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Track(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False)
    mp3_file = models.FileField(upload_to="uploads", blank=False, null=False)
    minutes = models.IntegerField(blank=False, null=False, validators=[MinValueValidator(0),
                                                                       MaxValueValidator(600)])
    seconds = models.IntegerField(blank=False, null=False, validators=[MinValueValidator(0),
                                                                       MaxValueValidator(60)])
    solo = models.BooleanField(blank=False, null=False, default=False)

    def save(self, *args, **kwargs):
        if self.solo == True:
            Track.objects.filter(solo=True).update(solo=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Playtime(models.Model):
    playtime_seconds = models.IntegerField(blank=False, null=False,
                                  default=20,
                                  validators=[MinValueValidator(0),
                                              MaxValueValidator(600)])
    def __str__(self):
        return str(self.playtime_seconds)
    

    def save(self, *args, **kwargs):
       self.pk = '0'
       super().save(*args, **kwargs)
