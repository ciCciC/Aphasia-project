
import AudioTranscribe
from Audio import Audio

def main():
    """
    To run the Main file from the terminal
    :return:
    """
    filepath = input('Enter filepath \n')
    hertz = input('Enter hertz \n')
    languageCode = input('Enter language code E.G. nl-NL or en-GB \n')
    chooseMethod = input('1: Google Storage 2: Audio file \n')

    if(chooseMethod == 1):
        # TODO filepath
        print(AudioTranscribe.AudioTranscribe.fromGoogleStorage(Audio('aphasiapatient.flac', hertz, languageCode)))
    elif(chooseMethod == 2):
        # TODO filepath
        AudioTranscribe.AudioTranscribe.fromAudioFile(Audio('aphasiapatientW.wav', hertz, languageCode))
    else:
        print('Something went wrong, please choose [1] or [2] or for exit [q]')
        if(input() == 'q'):
            exit(1)
        else:
            main()

main()

# print(AudioTranscribe.AudioTranscribe.fromGoogleStorage(Audio('aphasiapatient.flac', 16000, 'en-GB', enums.RecognitionConfig.AudioEncoding.FLAC)))
#
# AudioTranscribe.AudioTranscribe.fromAudioFile(Audio('aphasiapatientW.wav', 16000, 'en-GB', enums.RecognitionConfig.AudioEncoding.LINEAR16))