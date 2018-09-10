
from pydub import AudioSegment
import os
import numpy as np
from matplotlib import pyplot as plt

class Test:

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