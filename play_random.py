import os
import sys
import django
import random
import pygame
import time

track_path = './pb_ui/'
play_time = 10
sys.path.append(track_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'pb_ui.settings')
django.setup()
from mp3_manager.models import Track

all_tracks = Track.objects.all()
track = random.choice(all_tracks)

print(f"PLAYING: {track}")
print(track.name, track.mp3_file, track.minutes, track.seconds)

start_location = (int(track.minutes)*60) + int(track.seconds)
print(start_location)
clock = pygame.time.Clock()
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load(track_path+str(track.mp3_file))
pygame.mixer.music.play(start=start_location)
while pygame.mixer.music.get_busy():
    time.sleep(play_time)
    pygame.mixer.music.fadeout(2000)
pygame.event.wait()