import RPi.GPIO as GPIO
import os
import sys
import django
import pygame
import signal
import phue
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
               spotlights_channel, discoball_channel, b):
    print("Starting partying")
    # Initialise lights:
    playtime_obj = get_playtime_obj()
    hue_bridge_ip, hue_user_id, brightness = get_bridge_info()
    party_light_settings = get_light_settings()
    # Do things, i.e. after button press
    pb_lights = get_light_list(b)
    # loop over the lights and their settings and add them to this data structure
    # so we only have to do this once
    light_info = {}
    for light in pb_lights:
        for setting in party_light_settings:
            if light.name == setting.name:
                light_info[light.name] = {"light": light,
                                          "setting": setting}

    initial_light_settings = get_initial_colours(pb_lights)
    
    print("BUTTON: pressed")
    #possibly there should be some brief pauses before toggling things "on"
    if playtime_obj.music_only == False:
        print("DISCO BALL: on")
        GPIO.output(discoball_channel, GPIO.HIGH)
        print("SPOTLIGHTS: on")
        GPIO.output(spotlights_channel, GPIO.HIGH)
        print("DISCO LIGHT: on")
        GPIO.output(disco_lights_channel, GPIO.HIGH)
        GPIO.output(disco_lights_channel_2, GPIO.HIGH)
    
    if playtime_obj.lights_only == False:
        # get the set of track
        track_qset = get_tracks(playtime_obj.playlist_selection)
        print("MUSIC: on")
        #decide what set of tracks we are playing
        play_music(track_qset, playtime_obj, track_path, pygame, light_info, brightness)
    
    print("PARTY: off")
    print("MAIN LIGHTS: on\n")
    reset_lights(pb_lights, initial_light_settings)
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

    playtime_obj = get_playtime_obj()
    hue_bridge_ip, hue_user_id, brightness = get_bridge_info()
    b = phue.Bridge(hue_bridge_ip, hue_user_id)
    # Do things, i.e. after button press
    pb_lights = get_light_list(b)
    # loop over the lights and their settings and add them to this data
    # so we only have to do this once
    initial_light_settings = get_initial_colours(pb_lights)
    dip_lights(pb_lights)
    reset_lights(pb_lights, initial_light_settings)

    while True:
        if GPIO.input(input_channel):
            if toggle == 0:
                print("BUTTON: released\n")
            toggle=1
        else:
            toggle = lets_party(disco_lights_channel, disco_lights_channel_2,
                                spotlights_channel, discoball_channel, b)
            GPIO.setup(input_channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.setup(disco_lights_channel, GPIO.OUT)
            GPIO.setup(disco_lights_channel_2, GPIO.OUT)
            GPIO.setup(spotlights_channel, GPIO.OUT)
            GPIO.setup(discoball_channel, GPIO.OUT)