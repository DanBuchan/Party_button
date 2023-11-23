import librosa
import os
import time
import essentia.standard as es

def calc_tempo_librosa(audio_file, segment_dur_secs):
    y, sr = librosa.load(audio_file, sr=None, mono=True)
    print("FILE LOADED")
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

def calc_tempo_essentia(audio_file, segment_dur_secs):   
    audio = es.MonoLoader(filename=audio_file)()
    sr = 44100
    segment_length = sr * segment_dur_secs
    t = audio[0: segment_length]
    print("FILE LOADED")
    sum = 0
    for i in range(10):
        start = time.time()
        rhythm_extractor = es.RhythmExtractor2013(method="multifeature")
        # bpm, beats, beats_confidence, _, beats_intervals = rhythm_extractor(t)
        bpm = es.PercivalBpmEstimator()(t)
        end = time.time()
        time_delta=(end-start) % 60
        sum+=time_delta
        print(f"RUN TIME: {end-start}")
    print(f"MEAN TIME: {sum/10}")
    print("BPM:", bpm)

audio_dir = '/Users/dbuchan/Code/Party_button/pb_ui/example_data'
audio_file = os.path.join(audio_dir, 'katyperry_birthday.mp3')
   
#calc_tempo_librosa(audio_file, 30)
calc_tempo_essentia(audio_file, 10)
