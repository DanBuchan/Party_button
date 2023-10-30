import os
import sys
import django
import pygame
from music_lib import *

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
    play_music(track_qset, playtime_obj, track_path, pygame)


