import io
import os
import wave
import pyaudio
import numpy as np
from matplotlib import pyplot as plt

file_name = 'aphasiapatientW.wav'

file_path = os.path.join(
            os.path.dirname(__file__),
            'audio', file_name)

f = wave.open(file_path, 'r')
frames = f.getnframes()
rate = f.getframerate()
audioDuration = frames / float(rate)

with io.open(file_path, 'rb') as audio_file:
    contentSize = os.path.getsize(file_path)
    time = 60
    count = 0
    leftJump = 30
    CHUNCK_TIME = 60
    CHUNK_MEMORY = (contentSize / audioDuration) * CHUNCK_TIME

    x = 0
    y = 0

    timeZ = 0

    # while count < f.getnframes():
    #     timeZ += 60
    #     count += 1500
    #
    #     print((timeZ/60))
    print((f.getnframes()/f.getframerate())/500)
    print(audioDuration)

    # while count < f.getnframes():
    #
    #     tmpChunck = audio_file.read(CHUNK_MEMORY)
    #
    #     f.readframes()
    #
    #
    #
    #     count += time

def checkSignalWave(audiofile, x, y, f):
    tmpChunck = audio_file.read(CHUNK_MEMORY)

    a = wave.open(tmpChunck, 'r')

    audio_file.seek(0, 1)



signal = f.readframes(-1)
signal = np.fromstring(signal, 'Int16')

# print(len(signal[signal == 0]))

# plt.figure(1)
# plt.title('Signal Wave...')
# plt.plot(signal)
# plt.show()