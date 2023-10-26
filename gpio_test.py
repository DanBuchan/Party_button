import RPi.GPIO as GPIO
import time
import os
import sys
import django
import random
import pygame
import time

print("Setting Up")
track_path = './pb_ui/'
sys.path.append(track_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'pb_ui.settings')
django.setup()
from mp3_manager.models import Track, Playtime

all_tracks = Track.objects.all()

def play_music(all_tracks, play_time, track_path):
    play_track = random.choice(all_tracks)
    #override selection if one is soloing
    for track in all_tracks:
        if track.solo:
            play_track = track        

    print(f"PLAYING: {play_track}")
    print(play_track.name, play_track.mp3_file,
          play_track.minutes, play_track.seconds)

    start_location = (int(play_track.minutes)*60) + int(play_track.seconds)
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(track_path+str(play_track.mp3_file))
    pygame.mixer.music.play(start=start_location)
    while pygame.mixer.music.get_busy():
        time.sleep(play_time)
        pygame.mixer.music.stop()
    pygame.event.wait()

def lets_party(main_lights_channel, disco_lights_channel, spotlights_channel,
               discoball_channel):
    print("BUTTON: pressed")
    print("MAIN LIGHTS: off")
    GPIO.output(main_lights_channel, GPIO.HIGH)
    print("DISCO BALL: on")
    print("DISCO LIGHT: on")
    GPIO.output(disco_lights_channel, GPIO.HIGH)
    print("MUSIC: on")
    play_time = Playtime.objects.all()[0].playtime_seconds
    play_music(all_tracks, play_time, track_path)
    print("PARTY: off")
    print("MAIN LIGHTS: on")
    GPIO.output(disco_lights_channel, GPIO.LOW)
    GPIO.output(main_lights_channel, GPIO.LOW)
    toggle=0


GPIO.setmode(GPIO.BCM)
input_channel = 17
relay_channel = [22, 10]
main_lights_channel = 22
disco_lights_channel = 10
spotlights_channel = None
discoball_channel = None
GPIO.setup(input_channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(main_lights_channel, GPIO.OUT)
GPIO.setup(disco_lights_channel, GPIO.OUT)


toggle = 0
while True:
    if GPIO.input(input_channel):
        if toggle == 0:
            print("BUTTON: released\n")
        toggle=1
    else:
        lets_party(main_lights_channel, disco_lights_channel,
                   spotlights_channel, discoball_channel)