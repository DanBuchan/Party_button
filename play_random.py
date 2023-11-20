import os
import sys
import django
import pygame
from music_lib import *
import phue

track_path = './pb_ui/'

if __name__ == '__main__':
    # initialise things
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    playtime_obj = get_playtime_obj()
    hue_bridge_ip, hue_user_id, brightness = get_bridge_info()
    b = phue.Bridge(hue_bridge_ip, hue_user_id)
    party_light_settings = get_light_settings()
    
    # Do things, i.e. after button press
    pb_lights = get_light_list(b)
    initial_light_settings = get_initial_colours(pb_lights)
    #get the set of tracks
    track_qset = get_tracks(playtime_obj.playlist_selection)
    #decide what set of tracks we are playing
    if playtime_obj.lights_only == False:
        play_music(track_qset, playtime_obj, track_path, pygame, pb_lights, party_light_settings, brightness)
    reset_lights(pb_lights, initial_light_settings, None)
