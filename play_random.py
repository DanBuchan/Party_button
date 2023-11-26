import os
import sys
import django
import pygame
from music_lib import *
import phue
import pprint

track_path = './pb_ui/'
#
# test script for developing music_lib
#


if __name__ == '__main__':
    # initialise things
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    playtime_obj = get_playtime_obj()
    hue_bridge_ip, hue_user_id, name_stub, brightness = get_bridge_info()
    b = phue.Bridge(hue_bridge_ip, hue_user_id)
    party_light_settings = get_light_settings()
    
    pb_lights = get_light_list(b, name_stub)
    lights_data = b.get_api()["lights"]
    initial_light_settings = get_initial_colours(lights_data)
    
    dip_lights(pb_lights)
    reset_lights(pb_lights, initial_light_settings)

    
    # light_info = {}
    # for light in pb_lights:
    #     for setting in party_light_settings:
    #         if light.name == setting.name:
    #             light_info[light.name] = {"light": light,
    #                                       "setting": setting}

    exit()
    initial_light_settings = get_initial_colours(pb_lights)
    #get the set of tracks
    track_qset = get_tracks(playtime_obj.playlist_selection)
    #decide what set of tracks we are playing
    if playtime_obj.lights_only == False:
        play_music(track_qset, playtime_obj, track_path, pygame, light_info, brightness)
    else:
        pass
        #SHOULD RUN THE LIGHTS HERE        
    reset_lights(pb_lights, initial_light_settings)
