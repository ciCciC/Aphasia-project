
from pydub import AudioSegment
import os
import numpy as np
from matplotlib import pyplot as plt

class Test:

    file_name = os.path.join(
                os.path.dirname(__file__),
                'audio', 'aphasiapatientW.wav')

    sound = AudioSegment.from_wav(file_name)

    start = 0
    end = 60000
    MINUTE = 60000
    interval = 500
    silence_thresh = -40

    @staticmethod
    def getSlicedAudio(sound, start, end, interval, silence_thresh):
        """
        Method to loop backwards until a silence point is been found then it will return a sub audio from start till silence point
        :param sound: original audio file
        :param start: start of the sub audio
        :param end: is start + 1 minute
        :param interval: interval of a sub audio in milliseconds
        :param silence_thresh: to address where to slice
        :return: Dict with sub audio, leftpointer (end of de sub audio) and rightpointer
        """
        jumptLeft = interval

        for right in range(end, start, -interval):

            tmpJumpLeft = right-jumptLeft

            audio_slice = sound[tmpJumpLeft: right]

            if audio_slice.dBFS == -float('inf') or audio_slice.dBFS < silence_thresh:
                print('dBFS:{} - starttime:{} - endtime:{}'.format(audio_slice.dBFS, tmpJumpLeft, right))
                return {'audiochunk': sound[start: tmpJumpLeft], 'leftpointer': tmpJumpLeft, 'rightpointer': right}


    @staticmethod
    def runSlicing(sound, start, end, interval, silence_thresh, MINUTE):

        chunks = []

        while start < (sound.duration_seconds * 1000):

            slicedAudio = Test.getSlicedAudio(sound, start, end, interval, silence_thresh)

            audiochunk = slicedAudio['audiochunk']
            leftpointer = slicedAudio['leftpointer']
            rightpointer = slicedAudio['rightpointer']

            # TODO controleer de START = leftpointer en de END
            start = leftpointer

            end = (leftpointer + Test.MINUTE) if (leftpointer + MINUTE) < (sound.duration_seconds * 1000) else (sound.duration_seconds * 1000)

            chunks.append(audiochunk)


    @staticmethod
    def exportAudio(audio, filepath, fileName, format):
        if filepath[-1] != '\\' or filepath[-1] != '/':
            raise ValueError('Forgot to add / or \\ behind the Filepath.')
        audio.export(filepath + fileName + '.' + format, format=format)


    @staticmethod
    def drawGraph(data):
        data1 = []
        data2 = []
        for x in data:
            data1.append(x[0])
            data2.append(x[1])

        colors = np.random.rand(120)
        # plt.figure(1)
        plt.title('Signal Wave...')
        # plt.scatter(data2, data1, c=colors, alpha=5.5)
        figure = plt.gcf()
        plt.subplot()
        plt.stem(data2, data1)
        plt.show()
        figure.savefig('signal_wave_dbfs.png')