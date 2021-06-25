import librosa
import sox
import numpy as np
from pydub import AudioSegment
import soundfile as sf
import wavio
from scipy.io import wavfile

file_n = input("Enter the path of ur file :")
file_n1 = AudioSegment.from_mp3(file_n)
file_name = "./output/convertedFile.wav"
file_n1.export(file_name,format="wav")
mono_wav, sampling_rate = librosa.load(file_name, duration=270)
stereo_wav, sampling_rate = librosa.load(file_name, mono=False, duration=270)
tempo, beat_frames = librosa.beat.beat_track(y=stereo_wav[0], sr=sampling_rate)
length = mono_wav.shape[0]
end_of_beat = int((tempo / 120) * sampling_rate)
down_value = 0.17
amplitude_down_faster = np.linspace(1, down_value, 2*end_of_beat)
amplitude_up_faster = np.linspace(down_value, 1, 2*end_of_beat)
amplitude_down_slower = np.linspace(1, down_value, 4*end_of_beat)
amplitude_up_slower = np.linspace(down_value, 1, 4*end_of_beat)
left_up = False
right_up = False
left_maintain = False
right_maintain = True
i = 0
while i < length - 4*end_of_beat:
    fast = np.random.choice([True, False])
    if left_up:
        if fast:
            stereo_wav[0, i:i+(2*end_of_beat)] = mono_wav[i:i+(2*end_of_beat)]*amplitude_up_faster
            stereo_wav[1, i:i+(2*end_of_beat)] = mono_wav[i:i+(2*end_of_beat)]*amplitude_down_faster
            left_up = False
            left_maintain = True
            i += (2 * end_of_beat)
        else:                 
            stereo_wav[0, i:i+(4*end_of_beat)] = mono_wav[i:i+(4*end_of_beat)]*amplitude_up_slower
            stereo_wav[1, i:i+(4*end_of_beat)] = mono_wav[i:i+(4*end_of_beat)]*amplitude_down_slower
            left_up = False
            left_maintain = True
            i += (4 * end_of_beat)
    elif right_up:
        if fast:
            stereo_wav[1, i:i+(2*end_of_beat)] = mono_wav[i:i+(2*end_of_beat)]*amplitude_up_faster
            stereo_wav[0, i:i+(2*end_of_beat)] = mono_wav[i:i+(2*end_of_beat)]*amplitude_down_faster
            right_up = False
            right_maintain = True
            i += (2 * end_of_beat)
        else:
            stereo_wav[1, i:i+(4*end_of_beat)] = mono_wav[i:i+(4*end_of_beat)]*amplitude_up_slower
            stereo_wav[0, i:i+(4*end_of_beat)] = mono_wav[i:i+(4*end_of_beat)]*amplitude_down_slower
            right_up = False
            right_maintain = True
            i += (4 * end_of_beat)
    elif left_maintain:
        stereo_wav[0, i:i+end_of_beat] = mono_wav[i:i+end_of_beat]
        stereo_wav[1, i:i+end_of_beat] = mono_wav[i:i+end_of_beat]*down_value
        right_up = True
        left_maintain = False
        i += end_of_beat
    elif right_maintain:
        stereo_wav[1, i:i + end_of_beat] = mono_wav[i:i + end_of_beat]
        stereo_wav[0, i:i + end_of_beat] = mono_wav[i:i+end_of_beat]*down_value
        right_maintain = False
        left_up = True
        i += end_of_beat
stereo_wav[0, (length//(4*end_of_beat))*(4*end_of_beat):] *= 0.25
stereo_wav[1, (length//(4*end_of_beat))*(4*end_of_beat):] *= 0.25
wav1 = stereo_wav
wavfile.write('./output/outFile.wav', sampling_rate, wav1.T)
tfm = sox.Transformer()
tfm.treble(gain_db=5, slope=0.3)
tfm.bass(gain_db=5, slope=0.3)
tfm.build('./output/outFile.wav', './output/effectFile.wav')