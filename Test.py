import librosa
from pydub import AudioSegment
from pydub.playback import play
import numpy as np

from AudioConverter import AudioConverter
from AudioTranscribe import AudioTranscribe
from reader import reader
from store import datastore
import os
import scipy.io.wavfile as wavfile

def getTime(seconds, sample_rate):
    return int(seconds * sample_rate)

diphoneDir = '/Users/koray/PycharmProjects/AphasiaProject/diphones/'

filename = 'F60E2VT8'
file_name = reader.getFile('audio/'+filename, 'wav')
file_name = '/Users/koray/PycharmProjects/AphasiaProject/audiotest/nl-0023.wav'
audio = AudioSegment.from_wav(file_name)

y, sr = librosa.load(file_name)

toExport = y[getTime(2.55, sr):getTime(2.60, sr)]
toExport2 = y[getTime(0.90, sr):getTime(0.95, sr)]

# print(toExport)
export = np.concatenate((toExport, toExport2), axis=None)
librosa.output.write_wav(diphoneDir+"mashup1.wav", toExport2, sr)

test1 = audio[2550:2600]
test2 = audio[900:950]

con = test1
# con.export(diphoneDir+"mashup.wav", format="wav")

# play(con)