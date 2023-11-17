import sys
import os
import django
import random
import time
import colorsys

track_path = './pb_ui/'
sys.path.append(track_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'pb_ui.settings')
django.setup()
from mp3_manager.models import Track, Playtime, Playlist

def change_colour(pb_lights, party_light_settings, brightness, rand):
    colours = party_light_settings
    # step_interval = 60/bpm
    # num_steps = playtime/step_interval

    # we should loop over the lights, set the solid colour for the fixed ones
    # for the rest enter the infinite while loop and either make a rand change
    # or a stepped change, number of steps. For number of steps work out the
    # H and S interval and make that step each time
    if rand:
        while True:
            set_lights(pb_lights, colours, brightness)
            for i in range(len(colours)):
                colours[i][0] = random.randint(0, 65535)
                colours[i][1] = random.randint(0, 254)
            time.sleep(0.50)
    else:
        set_lights(pb_lights, colours, brightness)

def get_bridge_info():
    #we'll get this out of the party button UI later
    brightness = 0.25
    return "192.168.1.112", "GIRjjwwRjU7If6DYHwnzY2L6qxMOJnimt4Femjvd", int(254*brightness)

def get_light_list(b):
    light_list = []
    for light in b.lights:
        if "PB spot" in light.name:
            light_list.append(light)
    return light_list

def get_initial_colours(lights):
    initial_settings = []
    for i, light in enumerate(lights):
        initial_settings.append([light.hue, light.saturation, light.brightness ])
    return(initial_settings)

def set_lights(lights, settings, brightness):

    for i, light in enumerate(lights):
        light.hue = settings[i][0]
        light.saturation = settings[i][1]
        if brightness:
            light.brightness = brightness
        else:
            light.brightness = settings[i][2]    

def get_light_settings():
    R = 152
    G = 52
    B = 235
    hsv_values = colorsys.rgb_to_hsv(R/254, G/254, B/254)
    h = int(65535 * hsv_values[0])
    s = int(254 * hsv_values[1])
    v = int(254 * hsv_values[2])
    return [[h, s, v]]

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

def play_music(track_qset, playtime_obj, track_path, pygame):
    play_tracks = decide_playing_set(track_qset, playtime_obj)
    for track in play_tracks:
        print(f"PLAYING: {track}")
        print(f"FILE LOCATIONL: {track_path+str(track.mp3_file)}")
        pygame.mixer.music.load(track_path+str(track.mp3_file))
        play_duration, start_location = calculate_playing_coordinates(track, playtime_obj)
        print(f"STARTING PLAYBACK AT: {start_location} secs")
        print(f"PLAYING TRACK FOR: {play_duration} secs")
        pygame.mixer.music.play(start=start_location)
        time.sleep(play_duration)
        pygame.mixer.music.stop()
        print(f"PLAY FINISHED: {track}")
    return()