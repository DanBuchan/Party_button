# Generated by Django 4.2.6 on 2023-10-27 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mp3_manager', '0006_track_play_full'),
    ]

    operations = [
        migrations.AddField(
            model_name='track',
            name='mp3_length',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
