
from pydub import AudioSegment
from pydub.effects import normalize
from pydub.silence import detect_nonsilent
import numpy as np
from IPython.display import display
from IPython.display import Audio

def GetAudio(file , sr = 16000):
    return normalize(AudioSegment.from_file(file).set_frame_rate(sr))

def remove_Silence (audio,min_silence_len = 0.2):
    result = detect_nonsilent(audio,min_silence_len=int(min_silence_len*1000),silence_thresh=-60)
    newaudio = AudioSegment.empty()
    for index in result:
        newaudio += audio[index[0]:index[1]]
    return newaudio

def PrintAudioInfo(audio):
    channels = audio.channels
    sample_rate = audio.frame_rate
    print("Channels:", channels)
    print("Sample rate:", sample_rate)
    print("Duration: ", audio.duration_seconds)
    print("Bit depth:", audio.sample_width, "bits") 
    print("len samples:", len(np.array(audio.get_array_of_samples())))
    display(audio)