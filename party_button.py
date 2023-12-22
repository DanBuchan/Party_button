import RPi.GPIO as GPIO
import os
import sys
import django
import pygame
import signal
import phue
import time
import urllib.request
import ssl
from music_lib import *

print("Setting Up")
track_path = './pb_ui/'
sys.path.append(track_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'pb_ui.settings')
django.setup()
from mp3_manager.models import Track, Playtime, Playlist


def signal_term_handler(sigNum, frame):
    # on receiving a signal initiate a normal exit
    GPIO.cleanup()
    exit()

def lets_party(disco_lights_channel, disco_lights_channel_2,
               spotlights_channel, discoball_channel):
    print("Starting partying")
    # Get database info
    #before_func_time = time.time()
    playtime_obj = get_playtime_obj()
    hue_bridge_ip, hue_user_id, name_stub, room_name, brightness = get_bridge_info()
    party_light_settings = get_light_settings()
    groups = get_json(f'https://{hue_bridge_ip}/api/{hue_user_id}/groups', context)
    group_id = get_group_id(room_name, groups)
    initial_light_state = get_json(f'https://{hue_bridge_ip}/api/{hue_user_id}/lights', context)
    initial_scene_id = set_initial_scene(hue_bridge_ip, hue_user_id, initial_light_state, context)
    #after_func_time = time.time()
    #print(f"GET ALL STATE: {after_func_time-before_func_time}")

    print("BUTTON: pressed")
    #possibly there should be some brief pauses before toggling things "on"
    
    #time.sleep(0.3) - maybe need to pause here while lights do their thing.
      
    if playtime_obj.lights_only == False:
        # get the set of track
        track_qset = get_tracks(playtime_obj.playlist_selection)
        print("MUSIC: on")
        #decide what set of tracks we are playing
        # play_music(track_qset, playtime_obj, track_path, pygame,
        #            party_light_settings, brightness, hue_bridge_ip,
        #            hue_user_id, group_id)
        play_tracks = decide_playing_set(track_qset, playtime_obj)
        for track in play_tracks:
            print(f"PLAYING: {track}")
            print(f"FILE LOCATION: {track_path+str(track.mp3_file)}")
            pygame.mixer.music.load(track_path+str(track.mp3_file))
            play_duration, start_location = calculate_playing_coordinates(track, playtime_obj)
            print(f"STARTING PLAYBACK AT: {start_location} secs")
            print(f"PLAYING TRACK FOR: {play_duration} secs")
            proc = multiprocessing.Process(target=change_colour, args=(light_info, brightness, playtime_obj.playtime_seconds, track.bpm, hue_bridge_ip, hue_user_id, group_id))
            proc.start()
            pygame.mixer.music.set_volume(1.0)
            pygame.mixer.music.play(start=start_location)
            if playtime_obj.music_only == False:
                print("DISCO BALL: on")
                GPIO.output(discoball_channel, GPIO.HIGH)
                print("SPOTLIGHTS: on")
                GPIO.output(spotlights_channel, GPIO.HIGH)
                print("DISCO LIGHT: on")
                GPIO.output(disco_lights_channel, GPIO.HIGH)
                GPIO.output(disco_lights_channel_2, GPIO.HIGH)
            time.sleep(play_duration)
            pygame.mixer.music.stop()
            proc.terminate()
            print(f"PLAY FINISHED: {track}")
        
    print("PARTY: off")
    print("MAIN LIGHTS: on\n")
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
    
    # do we need a bit of a pause between these?
    GPIO.output(disco_lights_channel, GPIO.LOW)
    GPIO.output(disco_lights_channel_2, GPIO.LOW)
    GPIO.output(discoball_channel, GPIO.LOW)
    GPIO.output(spotlights_channel, GPIO.LOW)
    return(0)

if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    input_channel = 25
    disco_lights_channel = 15
    disco_lights_channel_2 = 23
    spotlights_channel = 18
    discoball_channel = 14
    GPIO.setup(input_channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(disco_lights_channel, GPIO.OUT)
    GPIO.setup(disco_lights_channel_2, GPIO.OUT)
    GPIO.setup(spotlights_channel, GPIO.OUT)
    GPIO.setup(discoball_channel, GPIO.OUT)
    
    toggle = 0
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    signal.signal(signal.SIGTERM, signal_term_handler)

    # get information from DB
    hue_bridge_ip, hue_user_id, name_stub, room_name, brightness = get_bridge_info()
    party_light_settings = get_light_settings()
    context = ssl._create_unverified_context()
    playtime_obj = get_playtime_obj()   

    # Get initial params to control lights
    initial_light_state = get_json(f'https://{hue_bridge_ip}/api/{hue_user_id}/lights', context)
    initial_scene_id = set_initial_scene(hue_bridge_ip, hue_user_id, initial_light_state, context)
    groups = get_json(f'https://{hue_bridge_ip}/api/{hue_user_id}/groups', context)
    group_id = get_group_id(room_name, groups)

    dip_lights(hue_bridge_ip, hue_user_id, group_id, initial_scene_id, context)
    pygame.mixer.music.load(track_path+'uploads/alert.mp3')
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play()
    time.sleep(2)
    
    input_zero_sequence_count = 0
    debounce_length = 10
    if playtime_obj.ghost:
        debounce_length = 1
    while True:
        input_data = GPIO.input(input_channel)
        
        if input_data == 0:
            input_zero_sequence_count += 1
        
        if input_data:
            if toggle == 0:
                print("BUTTON: released\n")
            toggle=1
        if input_zero_sequence_count == debounce_length:
            print("BUTTON: pressed\n")
            toggle = lets_party(disco_lights_channel, disco_lights_channel_2,
                                spotlights_channel, discoball_channel)
            GPIO.setup(input_channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.setup(disco_lights_channel, GPIO.OUT)
            GPIO.setup(disco_lights_channel_2, GPIO.OUT)
            GPIO.setup(spotlights_channel, GPIO.OUT)
            GPIO.setup(discoball_channel, GPIO.OUT)
            input_zero_sequence_count = 0