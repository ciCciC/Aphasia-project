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
import pandas as pd


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


def getSpeechFeatures(signal, sample_rate):
    mfcc_feat = mfcc(signal, sample_rate, winlen=0.010, nfft=580)
    d_mfcc_feat = delta(mfcc_feat, 2)

    # plt.hist(d_mfcc_feat[0:7,])

    plt.title('Non librosa')
    plt.tight_layout()

    plt.show()

    print(d_mfcc_feat)
    print(d_mfcc_feat.shape)


def getSpeechpyFeatures(signal, sample_rate):
    mfcc = speechpy.feature.mfcc(signal, sampling_frequency=sample_rate, frame_length=0.025, frame_stride=0.01,
                                 num_filters=26, fft_length=580, low_frequency=0, high_frequency=None)

    mfcc_feature_cube = speechpy.feature.extract_derivative_feature(mfcc)

    # print(mfcc_feature_cube[0].shape)
    #
    # print(mfcc_feature_cube.shape)

    return mfcc_feature_cube
    # plt.hist(mfcc_feature_cube[:,:,0])
    #
    # plt.title('Speechpy')
    # plt.tight_layout()
    #
    # plt.show()

def test(signal, sample_rate):
    temp3_energy = librosa.feature.melspectrogram(signal, sr=sample_rate, n_fft=580, n_mels=128).T
    temp3_energy = np.log(temp3_energy)
    temp3_mfcc = librosa.feature.mfcc(signal, sr=sample_rate, S=temp3_energy.T, n_mfcc=13, dct_type=2,
                                      n_fft=580,
                                      hop_length=0.01).T

    plt.hist(temp3_mfcc)

    plt.title('test')
    plt.tight_layout()

    plt.show()


def plotDiphone(signal, sample_rate):
    TimeSample = np.linspace(0, len(signal) / sample_rate, num=len(signal))

    plt.plot(TimeSample, signal, alpha=0.8, color='lime')

    plt.title('Diphone')
    plt.xlabel('Time')
    plt.ylabel('Signal')
    plt.tight_layout()

    plt.show()


folderpath = '/Users/koray/PycharmProjects/AphasiaProject/textfilestest/'
diphones = readDict(folderpath+'dataset.csv')


df=pd.read_csv(folderpath+'dataset.csv', sep=',', skiprows=1, names=['region', 'label', 'diphones', 'sample_rate'])
print(df['sample_rate'].dtypes)

mijn = df['region'][0]

mijn = [float(i) for i in mijn.split('|')]

for x in mijn:
    print(x)