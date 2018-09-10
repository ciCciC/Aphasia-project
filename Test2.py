import glob
import io
import os
import wave
import pyaudio
import numpy as np
from matplotlib import pyplot as plt
from pydub import AudioSegment

import AudioTranscribe
import Test

file_name = 'aphasiapatientW.wav'

file_path = os.path.join(
            os.path.dirname(__file__),
            'audio', file_name)

# f = wave.open(file_path, 'r')

# with io.open(file_path, 'rb') as audio_file:
#     contentSize = audio_file.read()
#
#
#
# signal = contentSize
# signal = np.fromstring(signal, 'Int16')
#
# plt.figure(1)
# plt.title('Signal Wave...')
# plt.plot(signal)
# plt.show()


# filedirectory = os.path.join(os.path.dirname(__file__),'temporary/')
#
# print(filedirectory)
#
# file_name = os.path.join(
#             os.path.dirname(__file__),
#             'audio', 'Bestandnaam.mp3')
#
# sound = AudioSegment.from_mp3(file_name)
#
# nieuweBestandnaam = 'nieuweBestandnaam'
#
# AudioTranscribe.exportAudio(sound,
#                             filedirectory,
#                             nieuweBestandnaam,
#                             'wav')