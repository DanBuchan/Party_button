from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class track(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False)
    mp3_file = models.FileField(upload_to="uploads", blank=False, null=False)
    minutes = models.IntegerField(blank=False, null=False)
    seconds = models.IntegerField(blank=False, null=False, validators=[MinValueValidator(0),
                                                                       MaxValueValidator(60)])
    minutes = models.IntegerField(blank=False, null=False, validators=[MinValueValidator(0),
                                                                       MaxValueValidator(600)])

    def __str__(self):
        return self.name
