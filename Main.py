import AudioTranscribe
from Audio import Audio

import sys

def main():
    """
    To run the Main file from the terminal
    :return:
    """

    # When the user provides system arguments at script startup, use those instead.
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
        hertz = int(sys.argv[2])
        languageCode = sys.argv[3]
        chooseMethod = int(sys.argv[4])
    else:
        filepath = input('Enter filepath \n')
        hertz = int(input('Enter hertz \n'))
        languageCode = input('Enter language code E.G. nl-NL or en-GB \n')
        chooseMethod = int(input('1: Google Storage 2: Audio file Sliced 3: Audio file Async \n'))

    # TODO if else statements, maybe switch-case statement ... ?
    if chooseMethod == 1:
        # TODO filepath
        print(AudioTranscribe.AudioTranscribe.fromGoogleStorage(Audio('aphasiapatient.flac', hertz, languageCode)))
    elif chooseMethod == 2:
        # TODO filepath
        AudioTranscribe.AudioTranscribe.fromAudioFile(Audio('aphasiapatientW.wav', hertz, languageCode))
    elif chooseMethod == 3:
        # TODO filepath
        AudioTranscribe.AudioTranscribe.testFromAudioAsync(Audio('aphasiapatientW.wav', hertz, languageCode))
    else:
        print('Something went wrong, please choose [1] or [2] or for exit [q]')
        if input() == 'q':
            exit(1)
        else:
            main()

# main()

# AudioTranscribe.AudioTranscribe.testFromAudioAsync(Audio('aphasiapatientW.wav', 16000, 'nl-NL'))

# print(AudioTranscribe.AudioTranscribe.fromGoogleStorage(Audio('aphasiapatient.flac', 16000, 'en-GB')))

# AudioTranscribe.AudioTranscribe.fromAudioFile(Audio('aphasiapatientW.wav', 16000, 'en-GB'))

AudioTranscribe.AudioTranscribe.transcribeFromSlicedAudio(Audio('aphasiapatientW.wav', 16000, 'en-GB'))
