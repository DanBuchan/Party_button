import os
import sys
import django
import random
import pygame
import time

track_path = './pb_ui/'
sys.path.append(track_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'pb_ui.settings')
django.setup()
from mp3_manager.models import Track, Playtime

play_time_object = Playtime.objects.all()[0]
play_time = play_time_object.playtime_seconds
print(play_time)

all_tracks = Track.objects.all()
play_track = random.choice(all_tracks)

#override selection if one is soloing
for track in all_tracks:
    if track.solo:
        play_track = track        

if play_track.override_playtime:
    play_time = play_track.playtime_seconds

print(f"PLAYING: {play_track}")
print(f"{play_track.mp3_file}\nSTART: {play_track.minutes}:{play_track.seconds}"
      f"\nPLAY TIME: {play_time}")
start_location = (int(play_track.minutes)*60) + int(play_track.seconds)
if play_time_object.play_full_override or play_track.play_full:
    start_location = 0
print(f"START LOACTION: {start_location}")
clock = pygame.time.Clock()
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load(track_path+str(play_track.mp3_file))
pygame.mixer.music.play(start=start_location)
while pygame.mixer.music.get_busy():
    if play_time_object.play_full_override or play_track.play_full:
        pass
    else:
        time.sleep(play_time)
        pygame.mixer.music.stop()
pygame.event.wait()