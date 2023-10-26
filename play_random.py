import os
import sys
import django
import random
from pydub import AudioSegment
from pydub.playback import play

track_path = './pb_ui/'
sys.path.append(track_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'pb_ui.settings')
django.setup()
from mp3_manager.models import Track, Playtime

play_time_object = Playtime.objects.all()[0]
play_time = play_time_object.playtime_seconds
print(play_time)

all_tracks = Track.objects.all()
play_track = random.choice(all_tracks)

#override selection if one is soloing
for track in all_tracks:
    if track.solo:
        play_track = track        

print(f"PLAYING: {play_track}")
song = AudioSegment.from_mp3(track_path+str(play_track.mp3_file))
duration = song.duration_seconds*1000
print(play_track.name, play_track.mp3_file,
      play_track.minutes, play_track.seconds)

start_location = ((int(play_track.minutes)*60) + int(play_track.seconds))*1000
play_duration = play_time*1000
end_location = start_location+play_duration

if play_time_object.play_full_override:
    print("GLOBAL FULL TRACK OVERRIDE TRIGGERED")
    end_location = duration
    start_location = 0

if play_track.override_playtime:
    print("PLAYING TRACK SPECIFIC PLAYTIME")
    end_location = start_location+play_track.playtime_seconds*1000
    print(f"PLAYING TRACK SPECIFIC PLAYTIME: {play_track.playtime_seconds}")

if play_track.play_full:
    print("PER TRACK FULL TRACK OVERRIDE TRIGGERED")
    end_location = duration
    start_location = 0

if end_location > duration:
    end_location = duration
if start_location > duration:
    start_location = duration-play_duration

song_segment = song[start_location:end_location]
play(song_segment)
print("PLAY FINISHED")
