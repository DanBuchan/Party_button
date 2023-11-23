import librosa
import os
import time

def calc_tempo(y, sr, segment_dur_secs):
    segment_length = sr * segment_dur_secs
    t = y[0: segment_length]
    sum = 0
    for i in range(10):
        start = time.time()
        tempo = librosa.feature.tempo(y=t, sr=sr)
        end = time.time()
        time_delta=(end-start) % 60
        sum+=time_delta
        print(f"RUN TIME: {end-start}")
    print(f"MEAN TIME: {sum/10}")
    print(tempo)

audio_dir = '/Users/dbuchan/Code/Party_button/pb_ui/example_data'
audio_file = os.path.join(audio_dir, 'katyperry_birthday.mp3')
y, sr = librosa.load(audio_file, sr=None) 
calc_tempo(y, sr, 15)
calc_tempo(y, sr, 30)
# calc_tempo(y, sr, 120)
