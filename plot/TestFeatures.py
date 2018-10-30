import glob, csv
import re

import librosa
import numpy as np
import speechpy
from librosa.feature import mfcc as MFCC
import matplotlib.pyplot as plt
import numpy as np
from librosa.display import specshow
from python_speech_features import mfcc
from python_speech_features import delta
from python_speech_features import logfbank
from python_speech_features import get_filterbanks
from python_speech_features import fbank
import pandas as pd
from scipy.fftpack import dct


def readDict(filepath):
    with open(filepath, 'r') as csvfile:
        return [sentence for sentence in csv.DictReader(csvfile)]


def getLibrosaFeatures(region, sample_rate):

    S = librosa.feature.melspectrogram(y=region, sr=sample_rate, n_mels=128, fmax=8000)

    # mfccs = MFCC(region, sample_rate, n_mfcc=40, dct_type=2, fmax=8000)
    mfccs = MFCC(S=librosa.power_to_db(S))

    fig = plt.figure(1)

    librosa.display.specshow(mfccs, x_axis='time')
    # plt.hist(mfccs)

    plt.colorbar()
    plt.title('Librosa')
    plt.tight_layout()

    plt.show()

    return mfccs


def getSpeechpyFeatures(signal, sample_rate):
    pre_emphasis = 0.97
    signal = np.append(signal[0], signal[1:] - pre_emphasis * signal[:-1])
    # speechpy.feature.filterbanks(num_filter=26, sampling_freq=sample_rate)
    # mfcc = speechpy.feature.mfcc(signal, sampling_frequency=sample_rate, num_filters=26, low_frequency=0, high_frequency=None)
    #
    # mfcc_feature_cube = speechpy.feature.extract_derivative_feature(mfcc)

    mfcc_feature_cube = speechpy.feature.mfcc(signal, sampling_frequency=sample_rate, num_filters=12)

    # print(mfcc_feature_cube[0].shape)
    #
    print(mfcc_feature_cube.shape)

    plt.hist(mfcc_feature_cube)

    plt.title('Speechpy')
    plt.tight_layout()

    plt.show()

    return mfcc_feature_cube


def getSpeechFeatures(signal, sample_rate):

    mfcc_feat = mfcc(signal, sample_rate, winlen=0.20, nfft=512)
    d_mfcc_feat = delta(mfcc_feat, 2)

    for x in d_mfcc_feat:
        plt.hist(x)

    print(d_mfcc_feat)

    plt.title('python_speech_features')
    plt.tight_layout()

    plt.show()


def plotBoundary(signal, sample_rate):

    TimeSample = np.linspace(0, len(signal) / sample_rate, num=len(signal))

    pre_emphasis = 0.97
    emphazied_signal = np.append(signal[0], signal[1:] - pre_emphasis * signal[:-1])

    plt.plot(TimeSample, signal, alpha=0.8, color='lime')
    plt.plot(TimeSample, emphazied_signal, alpha=0.8, color='red')

    plt.title('Diphone')
    plt.xlabel('Time')
    plt.ylabel('Signal')
    plt.tight_layout()

    plt.show()


def exportAudio(region, folderpath, name, sample_rate):
    exportName = folderpath + name + ".wav"
    librosa.output.write_wav(exportName, region, sample_rate)


folderpath = '/Users/koray/PycharmProjects/AphasiaProject/textfilestest/'
diphones = readDict(folderpath+'dataset.csv')


df = pd.read_csv(folderpath+'dataset.csv', sep=',', skiprows=1, names=['region', 'label', 'diphones', 'sample_rate'])
print(df['sample_rate'].dtypes)

data = df.loc[df.loc[:, 'label'] > 0, :]

mijn = np.array([float(i) for i in data.loc[0]['region'].split('|')])
rate = data.loc[0]['sample_rate']

# exportAudio(mijn, '/Users/koray/PycharmProjects/AphasiaProject/plot/', 'test', rate)

print(mijn.shape)

# test(mijn, rate)
# getSpeechpyFeatures(mijn, rate)
# plotBoundary(mijn, rate)
getSpeechFeatures(mijn, rate)