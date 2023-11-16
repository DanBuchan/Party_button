import os
import sys
import django
import pygame
from music_lib import *
import phue
import multiprocessing

track_path = './pb_ui/'
sys.path.append(track_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'pb_ui.settings')
django.setup()
from mp3_manager.models import Track, Playtime, Playlist

#https://discovery.meethue.com/
# "192.168.1.112"
# https://gist.github.com/jiaaro/faa96fabd252b8552066

if __name__ == '__main__':
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    playtime_obj = get_playtime_obj()
    hue_bridge_ip, hue_user_id, brightness = get_bridge_info()
    party_light_settings = get_light_settings()
    b = phue.Bridge(hue_bridge_ip, hue_user_id)
    pb_lights = get_light_list(b)
    initial_light_settings = get_initial_colours(pb_lights)
    proc = multiprocessing.Process(target=change_colour, args=(pb_lights, party_light_settings, brightness, True))
    proc.start()
    #get the set of track
    track_qset = get_tracks(playtime_obj.playlist_selection)
    #decide what set of tracks we are playing
    if playtime_obj.lights_only == False:
        play_music(track_qset, playtime_obj, track_path, pygame)
    proc.terminate()
    set_lights(pb_lights, initial_light_settings, None)
    

