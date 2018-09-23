from pydub import AudioSegment
from pydub.playback import play

import os

signals = {'p':'p', 'au':'au', 'w':'w'}

for x in signals:
    signals[x] = os.path.join(
            os.path.dirname(__file__),
            'audio', x + '.wav')

p = AudioSegment.from_wav(signals['p'])
au = AudioSegment.from_wav(signals['au'])
w = AudioSegment.from_wav(signals['w'])

# p = p[:(((p.duration_seconds/3))*1000)-100]
#
# w = w[:((w.duration_seconds/3)*1000)-100]

pauw = AudioSegment.empty()

pauw = p + au + w

play(pauw)