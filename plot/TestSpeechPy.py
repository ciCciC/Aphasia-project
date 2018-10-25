import scipy.io.wavfile as wav
import numpy as np
import speechpy
import matplotlib.pyplot as plt
import os

from reader import reader

def getTime(seconds, sample_rate):
    return int(seconds * sample_rate)

filename = 'F60E2VT8'
file_name = reader.getFile('audio/'+filename, 'wav')
fs, signal = wav.read(file_name)
signal = signal[0:getTime(3.5, fs)]

# Example of pre-emphasizing.
signal_preemphasized = speechpy.processing.preemphasis(signal, cof=0.98)

# Example of staching frames
# frames = speechpy.processing.stack_frames(signal, sampling_frequency=fs, frame_length=0.010, frame_stride=0.01, filter=lambda x: np.ones((x,)),
#          zero_padding=True)

# Example of extracting power spectrum
# power_spectrum = speechpy.processing.power_spectrum(frames, fft_points=512)
# print('power spectrum shape=', power_spectrum.shape)

############# Extract MFCC features #############
mfcc = speechpy.feature.mfcc(signal, sampling_frequency=fs, frame_length=0.010, frame_stride=0.01,
             num_filters=40, fft_length=512, low_frequency=0, high_frequency=None)

# mfcc_cmvn = speechpy.processing.cmvnw(mfcc, win_size=301,variance_normalization=True)
# print('mfcc(mean + variance normalized) feature shape=', mfcc_cmvn.shape)

mfcc_feature_cube = speechpy.feature.extract_derivative_feature(mfcc)
print('mfcc feature cube shape=', mfcc_feature_cube.shape)

# print(mfcc_feature_cube[200].ravel())

# oneD = mfcc_feature_cube[10].ravel()

print(mfcc[200])
print(mfcc_feature_cube[200])

plt.hist(mfcc)
plt.show()

# ############# Extract logenergy features #############
# logenergy = speechpy.feature.lmfe(signal, sampling_frequency=fs, frame_length=0.020, frame_stride=0.01,
#              num_filters=40, fft_length=512, low_frequency=0, high_frequency=None)
# logenergy_feature_cube = speechpy.feature.extract_derivative_feature(logenergy)
# print('logenergy features=', logenergy.shape)