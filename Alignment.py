import os
import glob
from pydub import AudioSegment
from pydub.silence import split_on_silence
from pydub.playback import play

def getAudioFiles(fileExtension='*'):
    """
    :param fileExtension: default = *, this takes all extensions in de folder. Enter mp3, wav, flac
    :return: list of audio files
    """
    return glob.glob(os.path.join(
        os.path.dirname(__file__), 'dutch/', '*.' + fileExtension))

def _calculate_peaks(audio_file):
    """ Returns a list of audio level peaks """
    chunk_length = len(audio_file) / 107

    loudness_of_chunks = [
        audio_file[i * chunk_length: (i + 1) * chunk_length].rms
        for i in range(107)]

    max_rms = max(loudness_of_chunks) * 1.00

    return [int((loudness / max_rms) * 60)
            for loudness in loudness_of_chunks]


def __startSlicedAudio(sound, interval, silence_thresh, cleanTime):
    """
    Method to loop backwards until a silence point is been found then it will return a sub audio from start till silence point
    :param sound: original audio file
    :param start: start of the sub audio
    :param end: is start + 1 minute
    :param interval: interval of a sub audio in milliseconds
    :param silence_thresh: to address where to slice
    :return: Dict with sub audio, leftpointer (end of de sub audio) and rightpointer
    """

    audioSegmenten = []
    jumpRight = interval
    left = 0
    end = sound.duration_seconds * 1000
    oldStart = 0
    increment = 1

    print('starttime:{} - endtime:{}'.format(left, end))

    while left < end:
        tmpJumpRight = left + jumpRight

        # audio_slice = sound[left: tmpJumpRight]
        audio_slice = sound[left]

        if abs(audio_slice.dBFS) > silence_thresh or audio_slice.dBFS == -float('inf'):
            print('Silence: {}  : Time: {}'.format(abs(audio_slice.dBFS), left))

        left += increment

    return audioSegmenten


audio = AudioSegment.from_wav(getAudioFiles(fileExtension='wav')[0])

# __startSlicedAudio(audio, 500, 40)

chunks = split_on_silence(audio_segment=audio, min_silence_len=800, silence_thresh=-43)
#
print('Length: ' + str(len(chunks)))

for x in chunks:
    play(x)


# def drawGraph(data):
#     import matplotlib.pyplot as plt
#     import numpy as np
#
#     signal = data.get_array_of_samples()
#     # signal = np.fromstring(signal, 'Int16')
#     signal = _calculate_peaks(data)
#     plt.title('Signal Wave...')
#     plt.plot(signal)
#     plt.show()
#
# drawGraph(audio)