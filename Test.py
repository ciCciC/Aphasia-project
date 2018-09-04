
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