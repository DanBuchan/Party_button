import sys
import os
import django
import random
import time
import multiprocessing

track_path = './pb_ui/'
sys.path.append(track_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'pb_ui.settings')
django.setup()

from mp3_manager.models import Playtime, Playlist, Bridge, Light

def change_colour(pb_lights, party_light_settings, brightness, playtime, bpm):
    # First up change the lights
    random_light_set = []
    fade_light_set = []
    for light in pb_lights:
        if party_light_settings[light.name]:
            if party_light_settings.random_colour:
                random_light_set.append(light)
            if party_light_settings.fade:
                fade_light_set.append(light)
            else:
                set_light(light, party_light_settings, brightness, playtime)

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
    while True:
        for light in random_light_set:
            if party_light_settings[light.name]['interval_size'] % step_count != 0:
                continue

            random_setting = {}
            random_setting[light.name]['primary_h'] = random.randint(0, 65535)
            random_setting[light.name]['primary_s'] = random.randint(0, 254)
            #check interval size modulo first
            if party_light_settings[light.name]['random_interval']:
                dice_roll = random.uniform(0, 1)
                if dice_roll == 1:
                    set_light(light, random_setting, brightness, None)
            else:
                set_light(light, random_setting, brightness, None)
        for light in fade_light_set:
            fade_setting = {}
            if step_count == 0:
                primary_ctl = False
            elif step_count % thirty_secs_steps == 0:
                if primary_ctl:
                    fade_setting[light.name]['primary_h'] = party_light_settings[light.name]['primary_h']
                    fade_setting[light.name]['primary_s'] = party_light_settings[light.name]['primary_s']
                    fade_setting[light.name]['secondary_h'] = party_light_settings[light.name]['secondary_h']
                    fade_setting[light.name]['secondary_s'] = party_light_settings[light.name]['secondary_s']
                    fade_setting[light.name]['fade'] = True
                    primary_ctl=False
                else:
                    fade_setting[light.name]['primary_h'] = party_light_settings[light.name]['secondary_h']
                    fade_setting[light.name]['primary_s'] = party_light_settings[light.name]['secondary_s']
                    fade_setting[light.name]['secondary_h'] = party_light_settings[light.name]['primary_h']
                    fade_setting[light.name]['secondary_s'] = party_light_settings[light.name]['primary_s']
                    fade_setting[light.name]['fade'] = True
                    fade_setting[light.name]['fade'] = True
                    primary_ctl=True  
            set_light(light, fade_setting, brightness, playtime)
                # set colours based on primary_ctl

        time.sleep(step_length)
        step_count += 1

def get_bridge_info():
    #we'll get this out of the party button UI later
    bridge = Bridge.objects.all().first()
    return bridge.ip, bridge.user_id, int(254*(bridge.brightness/100))

def get_light_list(b):
    light_list = []
    try:
        for light in b.lights:
            if "PB spot" in light.name:
                light_list.append(light)
    except Exception as e:
        print("Couldn't get live light list: "+str(e))
    return light_list

def get_initial_colours(lights):
    initial_settings = {}
    try:
        for light in enumerate(lights):
            initial_settings[light.name] = [light.hue, light.saturation, light.brightness ]
    except Exception as e:
        print("Unable to get initial light information:" + str(e))
    return(initial_settings)

def set_light(light, settings, brightness, playtime):
    if playtime > 30:
        playtime = 30
    light.hue = settings[light.name]['primary_h']
    light.saturation = settings[light.name]['primary_v']
    light.brightness = brightness
    if settings[light.name]['fade']:
        light.transitiontime = playtime*10
        light.hue = settings[light.name]['secondary_h']
        light.saturation = settings[light.name]['secondary_v']
        light.brightness = brightness
        

def reset_lights(light, settings, brightness, fade):

    for i, light in enumerate(lights):
        light.hue = settings[i][0]
        light.saturation = settings[i][1]
        if brightness:
            light.brightness = brightness
        else:
            light.brightness = settings[i][2]    


def get_light_settings():
    lights = Light.objects.all()
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

def play_music(track_qset, playtime_obj, track_path, pygame, pb_lights, party_light_settings, brightness):
    play_tracks = decide_playing_set(track_qset, playtime_obj)
    for track in play_tracks:
        print(f"PLAYING: {track}")
        print(f"FILE LOCATIONL: {track_path+str(track.mp3_file)}")
        pygame.mixer.music.load(track_path+str(track.mp3_file))
        play_duration, start_location = calculate_playing_coordinates(track, playtime_obj)
        print(f"STARTING PLAYBACK AT: {start_location} secs")
        print(f"PLAYING TRACK FOR: {play_duration} secs")
        proc = multiprocessing.Process(target=change_colour, args=(pb_lights, party_light_settings, brightness, playtime_obj.playtime_seconds, track.bpm))
        proc.start()
        pygame.mixer.music.play(start=start_location)
        time.sleep(play_duration)
        pygame.mixer.music.stop()
        proc.terminate()
        print(f"PLAY FINISHED: {track}")
    return()