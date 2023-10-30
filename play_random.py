import os
import sys
import django
import random
import pygame
import time
from button_lib import *

track_path = './pb_ui/'
sys.path.append(track_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'pb_ui.settings')
django.setup()
from mp3_manager.models import Track, Playtime, Playlist

if __name__ == '__main__':
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    playtime_obj = get_playtime_obj()
    #get the set of track
    track_qset = get_tracks(playtime_obj.playlist_selection)
    #decide what set of tracks we are playing
    play_tracks = decide_playing_set(track_qset, playtime_obj)
    for track in play_tracks:
        print(f"PLAYING: {track}")
        print(f"FILE LOCATIONL: {track_path+str(track.mp3_file)}")
        pygame.mixer.music.load(track_path+str(track.mp3_file))
        play_duration, start_location = calculate_playing_coordinates(track, playtime_obj)
        print(f"STARTING PLAYBACK AT: {start_location} secs")
        print(f"PLAYING TRACK FOR: {play_duration} secs")
        pygame.mixer.music.play(start=start_location)
        time.sleep(play_duration)
        pygame.mixer.music.stop()
        print(f"PLAY FINISHED: {track}")

