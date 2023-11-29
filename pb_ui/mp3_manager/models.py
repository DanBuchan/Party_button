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
    bpm = models.IntegerField(blank=False, null=False,
                                           default=0,
                                           validators=[MinValueValidator(0),
                                                       MaxValueValidator(400)])

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
    lights_only = models.BooleanField(blank=False, null=False, 
                                             default=False)
    music_only = models.BooleanField(blank=False, null=False, 
                                             default=False)
    ghost = models.BooleanField(blank=False, null=False, 
                                             default=False)
    # lights_only and music_only should really be a enum type


    def __str__(self):
        return str(self.playtime_seconds)

    def save(self, *args, **kwargs):
       self.pk = '0'
       super().save(*args, **kwargs)

class Bridge(models.Model):
    ip = models.CharField(max_length=200, default="127.0.0.0",
                          blank=False, null=False)
    user_id = models.CharField(max_length=200, default="XXXX",
                               blank=True, null=True)
    name_stub = models.CharField(max_length=200, default="party",
                                 blank=True, null=True)
    room = models.CharField(max_length=200, default="party",
                            blank=True, null=True)
    brightness = models.IntegerField(blank=False, null=False,
                                     default=0,
                                     validators=[MinValueValidator(0),
                                                 MaxValueValidator(100)])
    
    def __str__(self):
        return(self.ip)

class Light(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False)
    hue_bridge_id = models.IntegerField(blank=False, null=False,
                                    default=0,
                                    validators=[MinValueValidator(0),
                                                MaxValueValidator(254)])
    primary_R = models.IntegerField(blank=False, null=False,
                                    default=0,
                                    validators=[MinValueValidator(0),
                                                MaxValueValidator(254)])
    primary_G = models.IntegerField(blank=False, null=False,
                                    default=0,
                                    validators=[MinValueValidator(0),
                                                MaxValueValidator(254)])
    primary_B = models.IntegerField(blank=False, null=False,
                                    default=0,
                                    validators=[MinValueValidator(0),
                                                MaxValueValidator(254)])
    secondary_R = models.IntegerField(blank=False, null=False,
                                      default=0,
                                      validators=[MinValueValidator(0),
                                                  MaxValueValidator(254)])
    secondary_G = models.IntegerField(blank=False, null=False,
                                      default=0,
                                      validators=[MinValueValidator(0),
                                                  MaxValueValidator(254)])
    secondary_B = models.IntegerField(blank=False, null=False,
                                        default=0,
                                        validators=[MinValueValidator(0),
                                                    MaxValueValidator(254)])
    primary_H = models.IntegerField(blank=False, null=False,
                                    default=0,
                                    validators=[MinValueValidator(0),
                                                MaxValueValidator(65535)])
    primary_S = models.IntegerField(blank=False, null=False,
                                    default=0,
                                    validators=[MinValueValidator(0),
                                                MaxValueValidator(254)])
    primary_V = models.IntegerField(blank=False, null=False,
                                    default=0,
                                    validators=[MinValueValidator(0),
                                                MaxValueValidator(254)])
    secondary_H = models.IntegerField(blank=False, null=False,
                                      default=0,
                                      validators=[MinValueValidator(0),
                                                  MaxValueValidator(65535)])
    secondary_S = models.IntegerField(blank=False, null=False,
                                      default=0,
                                      validators=[MinValueValidator(0),
                                                  MaxValueValidator(254)])
    secondary_V = models.IntegerField(blank=False, null=False,
                                        default=0,
                                        validators=[MinValueValidator(0),
                                                    MaxValueValidator(254)])
    # primary, fade, randome and alternate should really be an enum class.
    primary_colour = models.BooleanField(blank=False, null=False, default=True) # only hold to primary colour
    fade = models.BooleanField(blank=False, null=False, default=False) # move between primary and secondary colour
    random_colour = models.BooleanField(blank=False, null=False, default=False) # Change between random colours
    alternate_colour = models.BooleanField(blank=False, null=False, default=False) # Alternate between colours

    random_interval = models.BooleanField(blank=False, null=False, default=False) # Only change on random intervals
    interval_size = models.IntegerField(blank=False, null=False,                # Change interval size
                                      default=1,
                                      validators=[MinValueValidator(1),
                                                  MaxValueValidator(254)])
    
    def __str__(self):
        return(self.name)
