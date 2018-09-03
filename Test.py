
import os
import glob
from ffmpy import FFmpeg

filepath = os.path.join(
    os.path.dirname(__file__),
    'video',
    'funnybikecrash.mp4')
#
# with open(filepath, 'x') as w:
#     w.write('lolz')


# a = glob.glob(os.path.join(
#             os.path.dirname(__file__), 'audio/','*.wav'))

a = glob.glob(os.path.join(
            os.path.dirname(__file__), 'video/','*.mp4'))

print(a)

print(filepath.title())

# print(filepath.title())

import subprocess

ff = FFmpeg(inputs={filepath.title(): None}, outputs={'output.wav': "-ab 160k -ac 2 -ar 44100 -vn"})

# ff.run()

command = "./ffmpeg -i " + a[0] + " -ab 160k -ac 2 -ar 44100 -vn audio.wav"

subprocess.call(command, shell=True)