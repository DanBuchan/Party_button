import os
import sys
import django
import pygame
from music_lib import *
import pprint
import urllib.request
import ssl
import json

track_path = './pb_ui/'
#
# test script for developing music_lib
#


if __name__ == '__main__':
    # initialise pygame things
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    
    # get information from DB
    playtime_obj = get_playtime_obj()
    hue_bridge_ip, hue_user_id, name_stub, room_name, brightness = get_bridge_info()
    party_light_settings = get_light_settings()
    track_qset = get_tracks(playtime_obj.playlist_selection)
    context = ssl._create_unverified_context()    

    # Get initial params to control lights
    initial_light_state = get_json(f'https://{hue_bridge_ip}/api/{hue_user_id}/lights', context)
    initial_scene_id = set_initial_scene(hue_bridge_ip, hue_user_id, initial_light_state, context)
    groups = get_json(f'https://{hue_bridge_ip}/api/{hue_user_id}/groups', context)
    group_id = get_group_id(room_name, groups)

    dip_lights(hue_bridge_ip, hue_user_id, group_id, initial_scene_id, context)

    exit()
    #get the set of tracks
    #decide what set of tracks we are playing
    if playtime_obj.lights_only == False:
        play_music(track_qset, playtime_obj, track_path, pygame, light_info, brightness)
    else:
        pass
        #SHOULD RUN THE LIGHTS HERE        
    
    # reset lights to initial state
    setting_data = f'{{"scene":"{initial_scene_id}", "transitiontime": 1}}'
    put(f'https://{hue_bridge_ip}/api/{hue_user_id}/groups/{group_id}/action', setting_data, context)
