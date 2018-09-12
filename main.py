
import glob
import os
import AudioTranscribe
from Audio import Audio
from ConfigSlicing import ConfigSlicing

import sys

def main():
    """
    A user input interface for terminal
    """

    # Import all audio files from audio folder
    files = glob.glob(os.path.join(
        os.path.dirname(__file__), 'audio/', '*.' + '*'))

    # show all audio files
    for i, x in enumerate(files):
        print(str(i + 1) + ') ' + x.title())

    filepath = ''
    hertz = 0
    languageCode = ''
    chooseMethod = 0

    # When the user provides system arguments at script startup, use those instead.
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
        hertz = int(sys.argv[2])
        languageCode = sys.argv[3]
        chooseMethod = int(sys.argv[4])
    else:
        filepath = files[int(input("Press the number of the audio file \n")) - 1]
        hertz = int(input('Enter hertz E.G. 16000 \n'))
        languageCode = input('Enter language code E.G. nl-NL or en-GB \n')
        chooseMethod = int(input('1) Google Storage audio \n2) Audio file Sliced \n3) Audio file Async \n'))


    if chooseMethod == 1:
        AudioTranscribe.AudioTranscribe.fromGoogleStorage(Audio(filepath, hertz, languageCode))

    elif chooseMethod == 2:
        AudioTranscribe.AudioTranscribe.fromAudioFile(Audio(filepath, hertz, languageCode))

    elif chooseMethod == 3:
        AudioTranscribe.AudioTranscribe.transcribeFromSlicedAudio(
            configAudio=Audio(filepath, hertz, languageCode),
            configSlicing=ConfigSlicing(0, 60000, 60000, 500, -40))

    else:
        print('Something went wrong, please choose [1] or [2] or for exit [q]')
        if input() == 'q':
            exit(1)
        else:
            main()
    pass


# main()

print(AudioTranscribe.AudioTranscribe.fromGoogleStorage(Audio('aphasiapatient.flac', 16000, 'en-GB')))

# AudioTranscribe.AudioTranscribe.fromAudioFile(Audio('aphasiapatientW.wav', 16000, 'en-GB'))

# AudioTranscribe.AudioTranscribe.transcribeFromSlicedAudio(Audio('aphasiapatientW.wav', 16000, 'en-GB'))
