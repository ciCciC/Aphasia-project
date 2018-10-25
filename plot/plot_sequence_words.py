import array
import decimal

import librosa
from scipy import fftpack
from scipy.io import wavfile
import matplotlib.pyplot as plt
import numpy as np
from reader import reader
from pydub import AudioSegment
from pydub.playback import play
import csv
import wave
from librosa.feature import mfcc as MFCC
from librosa.display import specshow
from librosa.feature import spectral_bandwidth

filename = 'F60E2VT8'
audioPath = reader.getFile('audio/'+filename, 'wav')
csvFile = reader.getFile('textfiles/'+filename, 'csv')

# sample_rate, signal = wavfile.read(audioPath)

# signal = signal[0:int(3.5 * sample_rate)]

# audioseg = AudioSegment.from_wav(audioPath)


def zoom(plt):
    # ax.margins(x=0, y=-0.25)
    fourS = 4.0
    twoS = 2.0
    plt.xlim(1.3, fourS)
    # plt.xlim(1.3, twoS-0.5)
    pass


def display_plot_audio_time(audio, rate, audiosegmenten):
    signal = audio

    Time = np.linspace(0, len(signal) / rate, num=len(signal))

    fig = plt.figure(1)

    plt.title('Phoneme boundary')
    plt.xlabel('Time (s)')
    plt.ylabel('Frequency (Hz)')

    ax = fig.add_subplot(111)

    zoom(plt)

    ax.plot(Time, signal, alpha=0.8, color='lime')

    ax.patch.set_facecolor('black')
    # ax.patch.set_alpha(0.5)

    xcoords = set()

    for x in audiosegmenten:
        xcoords.add(float(x[0]))
        xcoords.add(float(x[1]))

    linewidth = 2
    for xc in xcoords:
        plt.axvline(x=xc - 0.050, color='yellow', linestyle='--', linewidth=linewidth)
        plt.axvline(x=xc-0.005, color='blue', linestyle='--', linewidth=linewidth)
        plt.axvline(x=xc, color='red', linestyle='--', linewidth=linewidth)
        plt.axvline(x=xc + 0.005, color='blue', linestyle='--', linewidth=linewidth)
        plt.axvline(x=xc + 0.050, color='yellow', linestyle='--', linewidth=linewidth)

    filename = 'word_boundary_plot.png'
    fig.savefig(filename, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.tight_layout()
    plt.show()


def plotAudioSegment(audio, boundary, rate):
    frame_size = 0.025
    frame_step = frame_size * rate
    frame_step = int(round(frame_step))

    left = 5
    right = 5
    leftBig = 50
    rightBig = 50

    samples = audio[boundary-left:boundary+right].get_array_of_samples()
    leftSamples = audio[boundary-leftBig:boundary-left].get_array_of_samples()
    rightSamples = audio[boundary+right:boundary+rightBig].get_array_of_samples()

    TimeSample = np.linspace(0, len(samples) / rate, num=len(samples))
    TimeLeftSample = np.linspace(0, len(leftSamples) / rate, num=len(leftSamples))
    TimeRightSample = np.linspace(0, len(rightSamples) / rate, num=len(rightSamples))

    fig = plt.figure(1)

    # # Boundary 10 ms
    ax = fig.add_subplot(311)
    ax.plot(TimeSample, samples, alpha=0.8, color='lime')
    ax.set_title('Boundary sample')
    ax.patch.set_facecolor('black')

    # # Left 45 ms
    ax = fig.add_subplot(312)
    ax.plot(TimeLeftSample, leftSamples, alpha=0.8, color='lime')
    ax.set_title('Left sample')
    ax.patch.set_facecolor('black')

    # # Right 45 ms
    ax = fig.add_subplot(313)
    ax.plot(TimeRightSample, rightSamples, alpha=0.8, color='lime')
    ax.set_title('Right sample')
    ax.patch.set_facecolor('black')

    plt.tight_layout()
    plt.show()

def plotMFCC():
    y, sr = librosa.load(audioPath, duration=3.5)
    print('Y: {}'.format(y[0:1]))

    mfccs = MFCC(y, sr, n_mfcc=12, dct_type=2, fmax=8000)

    S, phase = librosa.magphase(librosa.stft(y=y))
    spectral = librosa.feature.spectral_bandwidth(S=S)

    fig = plt.figure(1)

    specshow(librosa.amplitude_to_db(S, ref=np.max), y_axis='log', x_axis='time')
    # librosa.display.specshow(librosa.amplitude_to_db(S, ref=np.max), y_axis='log', x_axis='time')

    plt.colorbar()
    plt.title('MFCC')
    plt.tight_layout()

    plt.show()

def plotPreComputedMFCC():
    y, sr = librosa.load(audioPath, duration=3.5)

    S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=256, fmax=8000)

    mfcc = MFCC(S=librosa.power_to_db(S))

    fig = plt.figure(1)

    specshow(mfcc, x_axis='time')

    plt.colorbar()
    plt.title('MFCC')
    plt.tight_layout()

    plt.show()


def plotSpectogram():
    y, sr = librosa.load(audioPath, duration=3.5)

    S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, fmax=8000)

    power_to_db = librosa.power_to_db(S, ref=np.max)

    fig = plt.figure(1)

    specshow(power_to_db, y_axis='mel', fmax=8000, x_axis='time')
    plt.hist(power_to_db)

    # plt.colorbar(format='%+2.0f dB')
    plt.title('MFCC')
    plt.tight_layout()

    plt.show()


def plotFFT(plotwav, rate):
    frame_size = 0.010
    frame_stride = 0.01
    pre_emphasis = 0.97
    emphasized_signal = np.append(signal[0], signal[1:] - pre_emphasis * signal[:-1])
    frame_length, frame_step = frame_size * sample_rate, frame_stride * sample_rate  # Convert from seconds to samples
    signal_length = len(emphasized_signal)
    frame_length = int(round(frame_length))
    frame_step = int(round(frame_step))
    num_frames = int(np.ceil(
        float(np.abs(signal_length - frame_length)) / frame_step))  # Make sure that we have at least 1 frame

    pad_signal_length = num_frames * frame_step + frame_length
    z = np.zeros((pad_signal_length - signal_length))
    pad_signal = np.append(emphasized_signal,
                              z)  # Pad Signal to make sure that all frames have equal number of samples without truncating any samples from the original signal

    indices = np.tile(np.arange(0, frame_length), (num_frames, 1)) + np.tile(
        np.arange(0, num_frames * frame_step, frame_step), (frame_length, 1)).T
    frames = pad_signal[indices.astype(np.int32, copy=False)]
    NFFT = 512

    frame = np.hamming(frame_length)

    mag_frames = np.absolute(np.fft.rfft(frame, NFFT))

    pow_frames = ((1.0 / NFFT) * ((mag_frames) ** 2))

    nfilt = 40

    low_freq_mel = 0
    high_freq_mel = (2595 * np.log10(1 + (sample_rate / 2) / 700))  # Convert Hz to Mel
    mel_points = np.linspace(low_freq_mel, high_freq_mel, nfilt + 2)  # Equally spaced in Mel scale
    hz_points = (700 * (10 ** (mel_points / 2595) - 1))  # Convert Mel to Hz
    bin = np.floor((NFFT + 1) * hz_points / sample_rate)

    fbank = np.zeros((nfilt, int(np.floor(NFFT / 2 + 1))))
    for m in range(1, nfilt + 1):
        f_m_minus = int(bin[m - 1])  # left
        f_m = int(bin[m])  # center
        f_m_plus = int(bin[m + 1])  # right

        for k in range(f_m_minus, f_m):
            fbank[m - 1, k] = (k - bin[m - 1]) / (bin[m] - bin[m - 1])
        for k in range(f_m, f_m_plus):
            fbank[m - 1, k] = (bin[m + 1] - k) / (bin[m + 1] - bin[m])
    filter_banks = np.dot(pow_frames, fbank.T)
    filter_banks = np.where(filter_banks == 0, np.finfo(float).eps, filter_banks)  # Numerical Stability
    filter_banks = 20 * np.log10(filter_banks)

    fig = plt.figure(1)
    ax = fig.add_subplot(311)
    ax.hist(filter_banks, alpha=0.8, color='lime')
    ax.set_title('Wavefile')
    ax.patch.set_facecolor('black')

    plt.show()

def getTime(seconds, sample_rate):
    return int(seconds * sample_rate)

def plotTestWavLib(wavaudio, wavsample, libaudio, libsample):
    t = np.arange(wavaudio.shape[0]) / float(wavsample)

    TimeSample = np.linspace(0, len(wavaudio) / wavsample, num=len(wavaudio))

    fig = plt.figure(1)

    ax = fig.add_subplot(311)
    ax.plot(t, wavaudio, alpha=0.8, color='lime')
    # ax.set_title('Boundary sample')
    ax.patch.set_facecolor('black')

    ax = fig.add_subplot(312)
    ax.plot(TimeSample, wavaudio, alpha=0.8, color='lime')
    # ax.set_title('Left sample')
    ax.patch.set_facecolor('black')

    plt.show()


audioseg = AudioSegment.from_wav(audioPath)

# fragments = [[x['begin'], x['end'], ''.join(x['word'])] for x in reader.readDict(csvFile)]

# plotAudioSegment(audioseg, 1000, audioseg.frame_rate)


plotMFCC()
# plotPreComputedMFCC()
# plotSpectogram()


sample_rate, signal = wavfile.read(audioPath)

starttime = 3.49

# signalwav = signal[getTime(starttime, sample_rate):getTime(3.5, sample_rate)]

# signaldub = audioseg[starttime * 1000:3500].get_array_of_samples()

# print('wav:{}'.format(signalwav))
# print('pydub:{}'.format(signaldub))

# y, sr = librosa.load(audioPath)

# plotTestWavLib(signal, sample_rate, y, sr)

# plotFFT(signal, sample_rate)

# display_plot_audio_time(audData, rate, fragments)