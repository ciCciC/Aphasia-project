

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
import os
import io
import glob
import wave
import Credentials

class AudioTranscribe:

    @staticmethod
    def fromGoogleStorage(ConfigAudio):
        """
        :param filename: filename of the audio file from Google Cloud Storage. The file has to be .FLAC or .WAV. Both has to be channel 1!!
        :param hertz: the hertz of the audio file
        :param languageCode: the languagecode for translating the text,, E.G. en-US or nl-NL
        :param audioEncoding: WAV = LINEAR16 and FLAC = FLAC
        :return: an array of transscript Strings
        """

        client = speech.SpeechClient(credentials=Credentials.Credentials.getCredentials())

        audio = types.RecognitionAudio(uri='gs://aphasiaproject/'+ConfigAudio.filename)

        config = types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
            sample_rate_hertz=ConfigAudio.hertz,
            profanity_filter=True,
            language_code=ConfigAudio.languageCode)

        operation = client.long_running_recognize(config, audio)

        print('Timeout 90s...')

        response = operation.result(timeout=90)

        text = []

        for result in response.results:
            for alternative in result.alternatives:
                text.append(alternative.transcript)

        return text


    @staticmethod
    def fromAudioFile(ConfigAudio):
        """
        TODO!! Getting all audio files from the 'audio' folder [NO URL or Google Cloud Storage] to iterate through and transform to text
        :param filename: filename of the audio file from the folder 'audio'. The file has to be .FLAC or .WAV. Both has to be channel 1!!
        :param hertz: the hertz of the audio file
        :param languageCode: the languagecode for translating the text,, E.G. en-US or nl-NL
        :param audioEncoding: WAV = LINEAR16 and FLAC = FLAC
        :return: an array of transscript Strings
        """

        file_name = os.path.join(
            os.path.dirname(__file__),
            'audio', ConfigAudio.filename)

        client = speech.SpeechClient(credentials=Credentials.Credentials.getCredentials())

        f = wave.open(file_name, 'r')
        frames = f.getnframes()
        rate = f.getframerate()
        audioDuration = frames / float(rate)

        with io.open(file_name, 'rb') as audio_file:
            contentSize = os.path.getsize(file_name)
            CHUNCK_TIME = 30
            CHUNK_MEMORY = (contentSize / audioDuration) * CHUNCK_TIME
            count = 0

            chuncks = []

            while count < audioDuration:
                chuncks.append(audio_file.read(int(CHUNK_MEMORY)))
                count += CHUNCK_TIME

            requests = (types.StreamingRecognizeRequest(audio_content=chunk)
                        for chunk in chuncks)

            config = types.RecognitionConfig(
                encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=ConfigAudio.hertz,
                language_code=ConfigAudio.languageCode,
                enable_word_time_offsets=True)

            streaming_config = types.StreamingRecognitionConfig(config=config)

            responses = client.streaming_recognize(streaming_config, requests)

            textDict = []

            # Get all responses and words of each response and timespan of each word
            for response in responses:
                for result in response.results:
                    print('Finished: {}'.format(result.is_final))
                    for alternative in result.alternatives:

                        for word_info in alternative.words:
                            word = word_info.word
                            start_time = word_info.start_time
                            end_time = word_info.end_time
                            print('Word: {}, start_time: {}, end_time: {}'.format(
                                word,
                                start_time.seconds,
                                end_time.seconds))

                            textDict.append({'word': word, 'starttime': str(start_time), 'endtime': str(end_time)})

                        # print(u'Transcript: {}'.format(alternative.transcript))
                        # text.append(alternative.transcript + '\n')
                        # text.append(str(start_time) + " - " + str(end_time) + " - " + str(word) + "\n")
        return textDict


    @staticmethod
    def getAudioFiles(fileExtension):
        return glob.glob(os.path.join(
            os.path.dirname(__file__), 'audio/','*.'+fileExtension))