# Generated by Django 4.2.6 on 2023-10-23 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mp3_manager', '0005_playtime_play_full_override_track_override_playtime_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='track',
            name='play_full',
            field=models.BooleanField(default=False),
        ),
    ]
