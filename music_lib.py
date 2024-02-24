import sys
import os
import django
import random
import time
import multiprocessing
import pprint
import urllib
import json
import ssl

track_path = './pb_ui/'
sys.path.append(track_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'pb_ui.settings')
django.setup()

from mp3_manager.models import Playtime, Playlist, Bridge, Light, DiscoLight

class Object(object):
    pass

def prep_scene_data(scenes, scene_name, light_info, control_type, brightness,
                    primary_ctl, randomctl=False):
    modify = False
    scene_id = None
    for id in scenes:
        if scenes[id]['name'] == scene_name:
            modify=True
            scene_id=id
    light_data = {}
    light_list = []
    light_on = True
    for light in light_info:
        light_brightness = brightness
        if light.off:
            light_on = False
        if light.override_brightness:
            light_brightness = int(254*(light.brightness/100))
        if light.randomise_brightness:
            light_brightness = random.randint(0, 254)
        if getattr(light, control_type):
            light_list.append(light.hue_bridge_id)
            if randomctl:
                light_data[light.hue_bridge_id] = {'state': { 'hue': random.randint(0, 65535),
                                                   'sat': random.randint(0, 254),
                                                   'bri': light_brightness,
                                                   'interval_size': light.interval_size,
                                                   'random_interval': light.random_interval,
                                                   'on': light_on,
                                                   }}
                continue
            if primary_ctl:
                light_data[light.hue_bridge_id] = {'state': {
                                                   'hue': light.primary_H,
                                                   'sat': light.primary_S,
                                                   'bri': light_brightness,
                                                   'interval_size': light.interval_size,
                                                   'random_interval': light.random_interval,
                                                   'on': light_on,
                                                   }}
            else:
                light_data[light.hue_bridge_id] = {'state': {'hue': light.secondary_H,
                                                   'sat': light.secondary_S,
                                                   'bri': light_brightness,
                                                   'interval_size': light.interval_size,
                                                   'random_interval': light.random_interval,
                                                   'on': light_on,
                                                    }}
                
    return {'modify': modify,
            'scene_id': scene_id,
            'light_list': light_list,
            'light_data': light_data}

def change_colour(light_info, brightness, playtime, bpm, ip, user, group_id):
    context = ssl._create_unverified_context()
    scene_url=f'https://{ip}/api/{user}/scenes'
    scenes = get_json(scene_url, context)

    static_scene_data = prep_scene_data(scenes, 'staticscene', light_info,
                                        'primary_colour', brightness, True)
    static_payload = create_scene_payload('staticscene',
                                          static_scene_data['light_list'],
                                          static_scene_data['light_data'],
                                          static_scene_data['modify'], )
    fade_scene_data1 = prep_scene_data(scenes, 'fadescene1', light_info,
                                        'fade', brightness, True)
    fade_payload1 = create_scene_payload('fadescene1',
                                          fade_scene_data1['light_list'],
                                          fade_scene_data1['light_data'],
                                          fade_scene_data1['modify'], )
    fade_scene_data2 = prep_scene_data(scenes, 'fadescene2', light_info,
                                        'fade', brightness, False)
    fade_payload2 = create_scene_payload('fadescene2',
                                          fade_scene_data2['light_list'],
                                          fade_scene_data2['light_data'],
                                          fade_scene_data2['modify'], )
    alternate_scene_data1 = prep_scene_data(scenes, 'alternatescene1', light_info,
                                            'alternate_colour', brightness, True)
    alternate_payload1 = create_scene_payload('alternatescene1',
                                          alternate_scene_data1['light_list'],
                                          alternate_scene_data1['light_data'],
                                          alternate_scene_data1['modify'], )
    alternate_scene_data2 = prep_scene_data(scenes, 'alternatescene2', light_info,
                                            'alternate_colour', brightness, False)
    random_scene_data = prep_scene_data(scenes, 'randomscene', light_info,
                                        'random_colour', brightness, True, True)
    random_payload = create_scene_payload('randomscene',
                                          random_scene_data['light_list'],
                                          random_scene_data['light_data'],
                                          random_scene_data['modify'], )

    if len(static_scene_data['light_list']) > 0:
        if static_scene_data['modify']:
            put(scene_url+"/"+static_scene_data['scene_id'], static_payload, context)
        else:
            create_response = post(scene_url, static_payload, context)
            static_scene_id = create_response[0]['success']['id']
            static_scene_data['scene_id'] = static_scene_id
        setting_data = f'{{"scene":"{static_scene_id}", "transitiontime": 1}}'
        put(f'https://{ip}/api/{user}/groups/{group_id}/action', setting_data, context)
    
    if len(fade_scene_data1['light_list']) > 0:
        if fade_scene_data1['modify']:
            put(scene_url+"/"+fade_scene_data1['scene_id'], fade_payload1, context)
        else:
            create_response = post(scene_url, fade_payload1, context)
            fade_scene_id = create_response[0]['success']['id']
            fade_scene_data1['scene_id'] = fade_scene_id
        if fade_scene_data2['modify']:
            put(scene_url+"/"+fade_scene_data2['scene_id'], fade_payload2, context)
        else:
            create_response = post(scene_url, fade_payload2, context)
            fade_scene_id = create_response[0]['success']['id']
            fade_scene_data2['scene_id'] = fade_scene_id
        scene_id = fade_scene_data1['scene_id']
        setting_data = f'{{"scene":"{scene_id}", "transitiontime": 1}}'
        put(f'https://{ip}/api/{user}/groups/{group_id}/action', setting_data, context)
    
    if len(alternate_scene_data1['light_list']) > 0:
        if alternate_scene_data1['modify']:
            put(scene_url+"/"+alternate_scene_data1['scene_id'], alternate_payload1, context)
        else:
            create_response = post(scene_url, alternate_payload1, context)
            alternate_scene_id = create_response[0]['success']['id']
            alternate_scene_data1['scene_id'] = alternate_scene_id
        scene_id = alternate_scene_data1['scene_id']
        setting_data = f'{{"scene":"{scene_id}", "transitiontime": 1}}'
        put(f'https://{ip}/api/{user}/groups/{group_id}/action', setting_data, context)
    
    if len(random_scene_data['light_list']) > 0:
        if random_scene_data['modify']:
            put(scene_url+"/"+random_scene_data['scene_id'], random_payload, context)
        else:
            create_response = post(scene_url, random_payload, context)
            random_scene_id = create_response[0]['success']['id']
            random_scene_data['scene_id'] = random_scene_id
        setting_data = f'{{"scene":"{random_scene_id}", "transitiontime": 1}}'
        put(f'https://{ip}/api/{user}/groups/{group_id}/action', setting_data, context)
    
    minute_portion=playtime/60
    steps = bpm*minute_portion
    step_length = playtime/steps
    step_count = 0
    transition_length = playtime*10 # set transition length and cap at 30 seconds
    if transition_length >= 300:
        transition_length = 300
    fade_primary = True
    thirty_secs_steps = int(30/step_length)
    
    if len(fade_scene_data1['light_list']) > 0:
        scene_id = fade_scene_data2['scene_id']
        setting_data = f'{{"scene":"{scene_id}", "transitiontime": {transition_length}}}'
        put(f'https://{ip}/api/{user}/groups/{group_id}/action', setting_data, context)
        fade_primary = False                  

    # booleans to track each light state
    light_primary_states = {}
    for light in light_info:
        if light.fade:
            light_primary_states[light.hue_bridge_id] = False
        else:
            light_primary_states[light.hue_bridge_id] = True
    while True:
        time.sleep(step_length)
        step_count += 1

        # deal with alternating lights
        alternating_data = {}
        if len(alternate_scene_data1['light_list']) > 0:
            for bulb_id in alternate_scene_data1['light_list']:
                dice_roll = 1
                if step_count % alternate_scene_data1['light_data'][bulb_id]['state']['interval_size'] == 0:
                    if alternate_scene_data1['light_data'][bulb_id]['state']['random_interval']:
                        dice_roll = random.randint(0, 1)
                    if dice_roll:
                        if light_primary_states[bulb_id]:
                            alternating_data[bulb_id] = {'state': { 'hue': alternate_scene_data2['light_data'][bulb_id]['state']['hue'],
                                                                    'sat': alternate_scene_data2['light_data'][bulb_id]['state']['sat'],
                                                                    'bri': alternate_scene_data2['light_data'][bulb_id]['state']['bri'],}}
                            light_primary_states[bulb_id] = False
                        else:
                            alternating_data[bulb_id] = {'state': { 'hue': alternate_scene_data1['light_data'][bulb_id]['state']['hue'],
                                                                    'sat': alternate_scene_data1['light_data'][bulb_id]['state']['sat'],
                                                                    'bri': alternate_scene_data1['light_data'][bulb_id]['state']['bri'],}}
                            light_primary_states[bulb_id] = True
                    else:
                        if light_primary_states[bulb_id]:
                            alternating_data[bulb_id] = {'state': { 'hue': alternate_scene_data1['light_data'][bulb_id]['state']['hue'],
                                                                'sat': alternate_scene_data1['light_data'][bulb_id]['state']['sat'],
                                                                'bri': alternate_scene_data1['light_data'][bulb_id]['state']['bri'],}}
                        else:
                            alternating_data[bulb_id] = {'state': { 'hue': alternate_scene_data2['light_data'][bulb_id]['state']['hue'],
                                                     'sat': alternate_scene_data2['light_data'][bulb_id]['state']['sat'],
                                                     'bri': alternate_scene_data2['light_data'][bulb_id]['state']['bri'],}}
                else:
                    if light_primary_states[bulb_id]:
                         alternating_data[bulb_id] = {'state': { 'hue': alternate_scene_data1['light_data'][bulb_id]['state']['hue'],
                                                                'sat': alternate_scene_data1['light_data'][bulb_id]['state']['sat'],
                                                                'bri': alternate_scene_data1['light_data'][bulb_id]['state']['bri'],}}
                    else:
                        alternating_data[bulb_id] = {'state': { 'hue': alternate_scene_data2['light_data'][bulb_id]['state']['hue'],
                                                     'sat': alternate_scene_data2['light_data'][bulb_id]['state']['sat'],
                                                     'bri': alternate_scene_data2['light_data'][bulb_id]['state']['bri'],}}

            alt_payload = create_scene_payload('alternatescene1',
                                          alternate_scene_data1['light_list'],
                                          alternating_data,
                                          True)
            put(scene_url+"/"+alternate_scene_data1['scene_id'], alt_payload, context)
            scene_id = alternate_scene_data1['scene_id']
            setting_data = f'{{"scene":"{scene_id}", "transitiontime": 1}}'
            put(f'https://{ip}/api/{user}/groups/{group_id}/action', setting_data, context)
        
        # deal with random lights
        random_data = {}
        if len(random_scene_data['light_list']) > 0:
            for bulb_id in random_scene_data['light_list']:
                dice_roll = 1
                if step_count % random_scene_data['light_data'][bulb_id]['state']['interval_size'] == 0:
                    if random_scene_data['light_data'][bulb_id]['state']['random_interval']:
                        dice_roll = random.randint(0, 1)
                    if dice_roll:
                        random_data[bulb_id] = {'state': {'hue': random.randint(0, 65535),
                                                          'sat': random.randint(0, 254),
                                                          'bri': random.randint(0, 254),}}
                    else:
                        random_data[bulb_id] = {'state': {'hue': random_scene_data['light_data'][bulb_id]['state']['hue'],
                                                          'sat': random_scene_data['light_data'][bulb_id]['state']['sat'],
                                                          'bri': random_scene_data['light_data'][bulb_id]['state']['bri'],}}
                else:
                    random_data[bulb_id] = {'state': {'hue': random_scene_data['light_data'][bulb_id]['state']['hue'],
                                                      'sat': random_scene_data['light_data'][bulb_id]['state']['sat'],
                                                      'bri': random_scene_data['light_data'][bulb_id]['state']['bri'],}}
            alt_payload = create_scene_payload('alternatescene1',
                                          random_scene_data['light_list'],
                                          random_data,
                                          True)
            put(scene_url+"/"+random_scene_data['scene_id'], alt_payload, context)
            scene_id = random_scene_data['scene_id']
            setting_data = f'{{"scene":"{scene_id}", "transitiontime": 1}}'
            put(f'https://{ip}/api/{user}/groups/{group_id}/action', setting_data, context)
        
        # handle fade if greater than 30 seconds
        if step_count % thirty_secs_steps == 0:
            if len(fade_scene_data1['light_list']) > 0:
                if fade_primary:
                    scene_id = fade_scene_data2['scene_id']
                    setting_data = f'{{"scene":"{scene_id}", "transitiontime": {transition_length}}}'
                    put(f'https://{ip}/api/{user}/groups/{group_id}/action', setting_data, context)
                    fade_primary = False                  
                else:
                    scene_id = fade_scene_data1['scene_id']
                    setting_data = f'{{"scene":"{scene_id}", "transitiontime": {transition_length}}}'
                    put(f'https://{ip}/api/{user}/groups/{group_id}/action', setting_data, context)
                    fade_primary = True                 
                    
def get_bridge_info():
    bridge = Bridge.objects.all().first()
    return bridge.ip, bridge.user_id, bridge.name_stub, bridge.room, \
           int(254*(bridge.brightness/100))

def put(url, content, context):
    """
    Do a HTTP PUT request with given content as payload.
    put(f'https://{ip}/api/{user}/lights/{light}/state', '{"on":true}')
    """
    req = urllib.request.Request(url=url,
        data=content.encode('UTF-8'), method='PUT')
    try_count = 0
    while True:
        if try_count == 30:
            break
        try:
            f = urllib.request.urlopen(req, context=context)
            break
        except Exception as e:
            try_count += 1
            print("Failed to PUT URL", str(e))
            print("URL: ", url)
            print("CONTENT", content.encode('UTF-8'))

    #print(f.status, f.reason, f.read())
    return json.loads(f.read())

def post(url, content, context):
    """
    Do a HTTP PUT request with given content as payload.
    put(f'https://{ip}/api/{user}/lights/{light}/state', '{"on":true}')
    """
    req = urllib.request.Request(url=url,
        data=content.encode('UTF-8'), method='POST')
    try_count = 0
    while True:
        if try_count == 30:
            break
        try:
            f = urllib.request.urlopen(req, context=context)
            break
        except Exception as e:
            try_count += 1
            print("Failed to POST URL", str(e))
            print("URL: ", url)
            print("CONTENT", content.encode('UTF-8'))
    #print(f.status, f.reason, f.read())
    return json.loads(f.read())

def get_json(url, context):
    """Do a HTTP GET request and return response parsed as JSON.
    get_json(f'https://{ip}/api/{user}/lights')
    """
    # print(url)
    req = urllib.request.Request(url=url, method='GET')
    try_count = 0
    while True:
        if try_count == 30:
            break
        try:
            f = urllib.request.urlopen(req, context=context)
            break
        except Exception as e:
            try_count += 1
            print("Failed to GET URL", str(e))
            print("URL: ", url)
    #print(f.status, f.reason)
    return json.loads(f.read())

def create_scene_payload(scene_name, light_ids, light_data, modify):
    payload = ''

    payload = f'{{"name": "{scene_name}", '
    if not modify:
        payload += '"recycle":false, '
    payload += '"lights": ['
    for light_id in light_ids:
        payload += f'"{light_id}", '
    payload = payload[:-2]+'], '
    payload += '"lightstates": {'
    lightstates = ''
    for light_id in light_ids:
        bri=light_data[light_id]['state']['bri']
        hue=light_data[light_id]['state']['hue'] 
        sat=light_data[light_id]['state']['sat']
        on=light_data[light_id]['state']['on']
        lightstates += f'"{light_id}": {{"bri": {bri}, "sat": {sat}, "hue": {hue}, "on": {on}}}, '
    payload += lightstates[:-2]+' } }'
    return payload

def set_initial_scene(ip, user, initial_lights, context):
    url=f'https://{ip}/api/{user}/scenes'

    scenes = get_json(f'https://{ip}/api/{user}/scenes', context)
    modify = False
    scene_id = None
    for id in scenes:
        if scenes[id]['name'] == 'initialscene':
            modify=True
            scene_id=id
        # req = urllib.request.Request(url=url+"/"+id, method='DELETE')
        # f = urllib.request.urlopen(req, context=context)
    
    payload = create_scene_payload('initialscene', initial_lights.keys(), initial_lights, modify)
    
    id = None
    if modify:
        put(url+"/"+scene_id, payload, context)
        id = scene_id
    else:
        create_response = post(url, payload, context)
        id = create_response[0]['success']['id']
    return (id)

def get_group_id(room_name, groups):
    for id in groups:
        print(id, room_name, groups[id]['name'])
        if room_name == groups[id]['name']:
            return id
    return None

def dip_lights(ip, user, group_id, initial_scene_id, context):
    setting_data = '{"bri":30, "transitiontime": 1}'
    put(f'https://{ip}/api/{user}/groups/{group_id}/action', setting_data, context)
    time.sleep(0.2)
    setting_data = f'{{"scene":"{initial_scene_id}", "transitiontime": 1}}'
    put(f'https://{ip}/api/{user}/groups/{group_id}/action', setting_data, context)

def get_light_settings():
    lights = Light.objects.all().order_by('name')
    return lights

def get_playtime_obj():
    '''
    Slightly pointless but return the playtime main object
    '''
    return(Playtime.objects.all()[0])

def get_tracks(playlist_name):
    '''
    return a list of tracks attached to a given playlist
    '''
    print(f"RETRIEVING PLAYLIST: {playlist_name}")
    playlist = Playlist.objects.filter(name=playlist_name)[0]
    tracks = playlist.track_set.all()
    return(tracks)

def return_active_lights():
    print(f"RETRIEVING DISCOLIGHTS")
    active_set = []
    lights = DiscoLight.objects.all()
    for light in lights:
        if light.light_on:
            active_set.append(light.pin_id)
    return(active_set)

def decide_playing_set(track_qset, playtime_obj):
    '''
    Set the set of tunes that we are going to play. Either pick one random tune,
    return all tunes in a playlist in a random order or return the one song that
    is set to 'solo'
    '''
    play_tracks = []
    for track in track_qset:
        play_tracks.append(track)
    if playtime_obj.play_whole_playlist:
        random.shuffle(play_tracks)
    else:
        play_tracks = [random.choice(play_tracks), ]

    for track in track_qset:
        if track.solo:
            play_tracks = [track, ] 
    return(play_tracks)

def calculate_playing_coordinates(track, playtime_obj):
    '''
    returns the playlocation start and the playtime duration
    '''
    track_duration = track.mp3_length/1000
    start_location = ((int(track.minutes)*60) + int(track.seconds))
    play_duration = playtime_obj.playtime_seconds
    
    if playtime_obj.play_full_override:
        print("GLOBAL FULL TRACK OVERRIDE TRIGGERED")
        play_duration = track_duration
        start_location = 0
    
    if track.override_playtime:
        play_duration = track.playtime_seconds
        print(f"PLAYING TRACK SPECIFIC PLAYTIME: {track.playtime_seconds}")
    
    if track.play_full:
        print("PER TRACK FULL TRACK OVERRIDE TRIGGERED")
        play_duration = track_duration
        start_location = 0
    
    if start_location+play_duration > track_duration:
        play_duration = track_duration-start_location
    
    if start_location > track_duration:
        start_location = track_duration-play_duration

    return(play_duration, start_location)

# def play_music(track_qset, playtime_obj, track_path, pygame, light_info, brightness, hue_bridge_ip, hue_user_id, group_id):
#     play_tracks = decide_playing_set(track_qset, playtime_obj)
#     for track in play_tracks:
#         print(f"PLAYING: {track}")
#         print(f"FILE LOCATION: {track_path+str(track.mp3_file)}")
#         pygame.mixer.music.load(track_path+str(track.mp3_file))
#         play_duration, start_location = calculate_playing_coordinates(track, playtime_obj)
#         print(f"STARTING PLAYBACK AT: {start_location} secs")
#         print(f"PLAYING TRACK FOR: {play_duration} secs")
#         proc = multiprocessing.Process(target=change_colour, args=(light_info, brightness, playtime_obj.playtime_seconds, track.bpm, hue_bridge_ip, hue_user_id, group_id))
#         proc.start()
#         pygame.mixer.music.play(start=start_location)
#         time.sleep(play_duration)
#         pygame.mixer.music.stop()
#         proc.terminate()
#         print(f"PLAY FINISHED: {track}")
#     return()