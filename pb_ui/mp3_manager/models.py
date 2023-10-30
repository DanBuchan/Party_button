from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Playlist(models.Model):
    name = models.CharField(max_length=256)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

class Track(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False)
    mp3_file = models.FileField(upload_to="uploads", blank=False, null=False)
    mp3_length = models.IntegerField(blank=True, null=True)
    minutes = models.IntegerField(blank=False, null=False, validators=[MinValueValidator(0),
                                                                       MaxValueValidator(600)])
    seconds = models.IntegerField(blank=False, null=False, validators=[MinValueValidator(0),
                                                                       MaxValueValidator(60)])
    solo = models.BooleanField(blank=False, null=False, default=False)
    play_full = models.BooleanField(blank=False, null=False, 
                                    default=False)
    override_playtime = models.BooleanField(blank=False, null=False,
                                            default=False)
    playtime_seconds = models.IntegerField(blank=False, null=False,
                                           default=0,
                                           validators=[MinValueValidator(0),
                                                       MaxValueValidator(600)])
    playlists = models.ManyToManyField(Playlist)
    
    def save(self, *args, **kwargs):
        if self.solo == True:
            Track.objects.filter(solo=True).update(solo=False)
        if self.play_full == True:
            result = Track.objects.filter(pk=self.pk)[0]
            if result.override_playtime == True:
                self.override_playtime = False
        if self.override_playtime == True:
            result = Track.objects.filter(pk=self.pk)[0]
            if result.play_full == True:
                self.play_full = False
                
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Playtime(models.Model):
    playtime_seconds = models.IntegerField(blank=False, null=False,
                                  default=20,
                                  validators=[MinValueValidator(0),
                                         
                                              MaxValueValidator(600)])
    play_full_override = models.BooleanField(blank=False, null=False, 
                                             default=False)
    play_whole_playlist = models.BooleanField(blank=False, null=False, 
                                             default=False)
    playlist_selection = models.ForeignKey(Playlist, null=True,
                                           on_delete=models.PROTECT)

    def __str__(self):
        return str(self.playtime_seconds)

    def save(self, *args, **kwargs):
       self.pk = '0'
       super().save(*args, **kwargs)