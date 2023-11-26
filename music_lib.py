import sys
import os
import django
import random
import time
import multiprocessing
import pprint

track_path = './pb_ui/'
sys.path.append(track_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'pb_ui.settings')
django.setup()

from mp3_manager.models import Playtime, Playlist, Bridge, Light

class Object(object):
    pass

def change_colour(light_info, brightness, playtime, bpm):
    # First up change the lights
    random_light_set = []
    fade_light_set = []
    alternate_light_set = []
    for light_name, light_details in light_info.items():
        if light_details['setting'].random_colour:
            random_light_set.append(light_details)
        elif light_details['setting'].fade:
            fade_light_set.append(light_details)
        elif light_details['setting'].alternate_colour:
            alternate_light_set.append(light_details)    
        else:
            set_light(light_details, brightness, 1, True)

    # we should loop over the lights, set the solid colour for the fixed ones
    # for the rest enter the infinite while loop and either make a rand change
    # or a stepped change, number of steps. For number of steps work out the
    # H and S interval and make that step each time
    # initial steps per minute is the bpm
    minute_portion=playtime/60
    steps = bpm*minute_portion
    step_length = playtime/steps
    step_count = 0
    thirty_secs_steps = int(30/step_length)
    primary_ctl = True
    #workout number of steps in 
    alternate_tracker = {}
    fade_tracker = {}
    while True:
        for light_settings in alternate_light_set:
            dice_roll = 1
            if light_settings['setting'].random_interval:
                dice_roll = random.randint(0, 1)
            
            if step_count == 0:
                set_light(light_settings, brightness, 1, True)
                alternate_tracker[light_settings['setting'].name] = True
            if step_count % light_settings['setting'].interval_size == 0:
                if alternate_tracker[light_settings['setting'].name]:
                    if dice_roll:
                        set_light(light_settings, brightness, 1, False)
                        alternate_tracker[light_settings['setting'].name] = False
                else:
                    if dice_roll:
                        set_light(light_settings, brightness, 1, True)
                        alternate_tracker[light_settings['setting'].name] = True
        
        for light_settings in fade_light_set:
            if step_count == 0:
                set_light(light_settings, brightness, 1, True)
                transition_length = playtime*10
                # currently capping the transition length to 30.
                if transition_length >= 300:
                    transition_length = 300
                set_light(light_settings, brightness, transition_length , False)
                fade_tracker[light_settings['setting'].name] = False
            elif step_count % thirty_secs_steps == 0:
                if fade_tracker[light_settings['setting'].name]:
                    set_light(light_settings, brightness, transition_length, False)
                    fade_tracker[light_settings['setting'].name] = False
                else:
                    set_light(light_settings, brightness, transition_length, True)
                    fade_tracker[light_settings['setting'].name] = True

        for light_settings in random_light_set:
            dice_roll = 1
            if light_settings['setting'].random_interval:
                dice_roll = random.randint(0, 1)
            
            random_setting = {'light': light_settings['light'],
                              'setting': Object()}
            random_setting['setting'].primary_H = random.randint(0, 65535)
            random_setting['setting'].primary_S = random.randint(0, 254)
            
            if step_count == 0:
                set_light(random_setting, brightness, 1, True)
            elif step_count % light_settings['setting'].interval_size == 0:
                random_setting['setting'].primary_H = random.randint(0, 65535)
                random_setting['setting'].primary_S = random.randint(0, 254)
                if dice_roll:
                    set_light(random_setting, brightness, 1, True)
        time.sleep(step_length)
        step_count += 1


def get_bridge_info():
    bridge = Bridge.objects.all().first()
    return bridge.ip, bridge.user_id, bridge.name_stub, bridge.room, \
           int(254*(bridge.brightness/100))

def get_light_list(b, name_stub):
    light_list = [None] * len(b.lights)
    try:
        for light in b.lights:
            if name_stub in light.name:
                bits = light.name.split()
                light_list[int(bits[-1])-1] = light
    except Exception as e:
        print("Couldn't get live light list: "+str(e))
    return light_list

def get_initial_colours(lights):
    initial_settings = {}
    # pprint.pprint(lights)
    try:
        for light in lights:
            initial_settings[lights[light]["name"]] = [lights[light]["state"]["hue"],
            lights[light]["state"]["sat"], lights[light]["state"]["bri"] ]
    except Exception as e:
        print("Unable to get initial light information:" + str(e))
    return(initial_settings)

def set_light(light_setting, brightness, transition_time=1, primary=True):
    light = light_setting['light']
    settings = light_setting['setting']
    if primary:
        light.transitiontime = transition_time 
        light.hue = settings.primary_H
        light.saturation = settings.primary_S   
        light.brightness = brightness
    else:
        light.transitiontime = transition_time
        light.hue = settings.secondary_H
        light.saturation = settings.secondary_S
        light.brightness = brightness
        
def reset_lights(lights, settings):
    for light in lights:
        if light.name in settings:
            light.transitiontime = 1
            light.hue = settings[light.name][0]
            light.saturation = settings[light.name][1]
            light.brightness = settings[light.name][2]    

def dip_lights(lights):
    for light in lights:
        print(light.name)
        light.transitiontime = 1
        light.hue = 0
        light.saturation = 0
        light.brightness = 0            

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

def play_music(track_qset, playtime_obj, track_path, pygame, light_info, brightness):
    play_tracks = decide_playing_set(track_qset, playtime_obj)
    for track in play_tracks:
        print(f"PLAYING: {track}")
        print(f"FILE LOCATION: {track_path+str(track.mp3_file)}")
        pygame.mixer.music.load(track_path+str(track.mp3_file))
        play_duration, start_location = calculate_playing_coordinates(track, playtime_obj)
        print(f"STARTING PLAYBACK AT: {start_location} secs")
        print(f"PLAYING TRACK FOR: {play_duration} secs")
        proc = multiprocessing.Process(target=change_colour, args=(light_info, brightness, playtime_obj.playtime_seconds, track.bpm))
        proc.start()
        pygame.mixer.music.play(start=start_location)
        time.sleep(play_duration)
        pygame.mixer.music.stop()
        proc.terminate()
        print(f"PLAY FINISHED: {track}")
    return()