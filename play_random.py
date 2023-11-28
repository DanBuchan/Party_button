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

    pygame.mixer.music.load(track_path+'uploads/alert.mp3')
    pygame.mixer.music.play()
    dip_lights(hue_bridge_ip, hue_user_id, group_id, initial_scene_id, context)
    time.sleep(0.5)
    
    #get the set of tracks
    #decide what set of tracks we are playing
    
    exit()
    if playtime_obj.lights_only == False:
        play_music(track_qset, playtime_obj, track_path, pygame,
                   party_light_settings, brightness, hue_bridge_ip,
                   hue_user_id, group_id)
    else:
        pass
        #SHOULD RUN THE LIGHTS HERE        
    
    # reset lights to initial state
    
    # # set main lights back where you found them
    setting_data = f'{{"scene":"{initial_scene_id}", "transitiontime": 1}}'
    put(f'https://{hue_bridge_ip}/api/{hue_user_id}/groups/{group_id}/action',
        setting_data, context)

    # # DELETE ALL SCENES
    scenes_url=f'https://{hue_bridge_ip}/api/{hue_user_id}/scenes'
    scenes = get_json(scenes_url, context)
    for id in scenes:
        if scenes[id]['name'] == 'initialscene' or \
           scenes[id]['name'] == 'fadescene1' or \
           scenes[id]['name'] == 'fadescene2' or \
           scenes[id]['name'] == 'staticscene' or \
           scenes[id]['name'] == 'alternatescene1' or \
           scenes[id]['name'] == 'alternatescene2' or \
           scenes[id]['name'] == 'randomscene':
            req = urllib.request.Request(url=scenes_url+"/"+id, method='DELETE')
            f = urllib.request.urlopen(req, context=context)
    