import RPi.GPIO as GPIO
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

def play_music(all_tracks, play_time_obj, track_path):
    play_track = random.choice(all_tracks)
    #override selection if one is soloing
    for track in all_tracks:
        if track.solo:
            play_track = track        

    print(f"PLAYING: {play_track}")
    track_duration = play_track.mp3_length/1000
    print(play_track.name, play_track.mp3_file,
          play_track.minutes, play_track.seconds)
    print(track_path+str(play_track.mp3_file))
    pygame.mixer.music.load(track_path+str(play_track.mp3_file))
    
    start_location = ((int(play_track.minutes)*60) + int(play_track.seconds))
    play_duration = play_time_obj.playtime_seconds
    
    if play_time_obj.play_full_override:
        print("GLOBAL FULL TRACK OVERRIDE TRIGGERED")
        play_duration = track_duration
        start_location = 0
    
    if play_track.override_playtime:
        print("PLAYING TRACK SPECIFIC PLAYTIME")
        play_duration = play_track.playtime_seconds
        print(f"PLAYING TRACK SPECIFIC PLAYTIME: {play_track.playtime_seconds}")
    
    if play_track.play_full:
        print("PER TRACK FULL TRACK OVERRIDE TRIGGERED")
        play_duration = track_duration
        start_location = 0
    
    if start_location+play_duration > track_duration:
        play_duration = track_duration-start_location
    
    if start_location > track_duration:
        start_location = track_duration-play_duration
    
    print(f"PLAYING TRACK FOR: {play_duration} secs")
    pygame.mixer.music.play(start=start_location)
    time.sleep(play_duration)
    pygame.mixer.music.stop()
    print("PLAY FINISHED")
    return()


def lets_party(main_lights_channel, disco_lights_channel, spotlights_channel,
               discoball_channel):
    print("BUTTON: pressed")
    print("MAIN LIGHTS: off")
    GPIO.output(main_lights_channel, GPIO.HIGH)
    print("DISCO BALL: on")
    print("DISCO LIGHT: on")
    GPIO.output(disco_lights_channel, GPIO.HIGH)
    print("MUSIC: on")
    play_time_obj = Playtime.objects.all()[0]
    all_tracks = Track.objects.all()
    play_music(all_tracks, play_time_obj, track_path)
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
    while True:
        if GPIO.input(input_channel):
            if toggle == 0:
                print("BUTTON: released\n")
            toggle=1
        else:
            lets_party(main_lights_channel, disco_lights_channel,
                       spotlights_channel, discoball_channel)