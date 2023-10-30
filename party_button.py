import RPi.GPIO as GPIO
import os
import sys
import django
import pygame
import signal
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

def lets_party(main_lights_channel, disco_lights_channel, spotlights_channel,
               discoball_channel):
    print("BUTTON: pressed")
    print("MAIN LIGHTS: off")
    GPIO.output(main_lights_channel, GPIO.HIGH)
    print("DISCO BALL: on")
    print("DISCO LIGHT: on")
    GPIO.output(disco_lights_channel, GPIO.HIGH)
    print("MUSIC: on")
    
    playtime_obj = get_playtime_obj()
    #get the set of track
    track_qset = get_tracks(playtime_obj.playlist_selection)
    #decide what set of tracks we are playing
    play_music(track_qset, playtime_obj, track_path, pygame)    
    
    print("PARTY: off")
    print("MAIN LIGHTS: on\n")
    GPIO.output(disco_lights_channel, GPIO.LOW)
    GPIO.output(main_lights_channel, GPIO.LOW)
    toggle=0

if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    input_channel = 17
    main_lights_channel = 22
    disco_lights_channel = 10
    spotlights_channel = None
    discoball_channel = None
    GPIO.setup(input_channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(main_lights_channel, GPIO.OUT)
    GPIO.setup(disco_lights_channel, GPIO.OUT)
    
    toggle = 0
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    signal.signal(signal.SIGTERM, signal_term_handler)
    
    while True:
        if GPIO.input(input_channel):
            if toggle == 0:
                print("BUTTON: released\n")
            toggle=1
        else:
            lets_party(main_lights_channel, disco_lights_channel,
                       spotlights_channel, discoball_channel)