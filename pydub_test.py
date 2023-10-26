from pydub import AudioSegment
from pydub.playback import play

song = AudioSegment.from_mp3("/Users/dbuchan/Code/Party_button/pb_ui/example_data/50cent_InDaClub.mp3")
duration = song.duration_seconds*1000
print(f"LENGTH: {duration}")
start_min = 4 
start_sec = 0
playtime = 5
start = ((start_min*60)+start_sec)*1000
play_duration = playtime*1000
end = start+play_duration

if end > duration:
   end = duration

if start > duration:
   start = duration-play_duration

song_segment = song[start:end]
play(song_segment)
