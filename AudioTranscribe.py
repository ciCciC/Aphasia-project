
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

import os
import io
import wave
import csv

from pydub import AudioSegment

import Credentials
from store.datastore import datastore


class AudioTranscribe:

    @staticmethod
    def fromGoogleStorage(ConfigAudio, enable_word_time):
        """
        :param filename: filename of the audio file from Google Cloud Storage. The file has to be .FLAC or .WAV. Both has to be channel 1!!
        :param hertz: the hertz of the audio file
        :param languageCode: the languagecode for translating the text,, E.G. en-US or nl-NL
        :param audioEncoding: WAV = LINEAR16 and FLAC = FLAC
        :return: an array of transscript Strings
        """

        print('Adding audio file in progress.....')
        datastore.addAudioFile(file_name=ConfigAudio.filename, fileFormat=ConfigAudio.fileFormat)

        client = speech.SpeechClient(credentials=Credentials.Credentials.getCredentials())

        audio = types.RecognitionAudio(uri='gs://aphasia-project/'+ConfigAudio.filename)

        config = types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
            sample_rate_hertz=16000,
            profanity_filter=False,
            language_code=ConfigAudio.languageCode,
            enable_word_time_offsets=enable_word_time)

        operation = client.long_running_recognize(config, audio)

        print('Transcribing in progress.....')
        response = operation.result(timeout=90)

        text = [alternative for result in response.results for alternative in result.alternatives]

        if enable_word_time:
            print('CSV in progress.....')
            AudioTranscribe.__save_in_csv(filename=ConfigAudio.filename, text=text)
        else:
            print('Txt in progress.....')
            AudioTranscribe.__save_in_txt(filename=ConfigAudio.filename, text=text)

        print('Deleting audio file in progress.....')
        datastore.deleteAudioFile(file_name=ConfigAudio.filename)

        pass


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

            chunks = []

            while count < audioDuration:
                chunks.append(audio_file.read(int(CHUNK_MEMORY)))
                count += CHUNCK_TIME

            requests = (types.StreamingRecognizeRequest(audio_content=chunk)
                        for chunk in chunks)

            config = types.RecognitionConfig(
                encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=ConfigAudio.hertz,
                language_code=ConfigAudio.languageCode,
                enable_word_time_offsets=True)

            streaming_config = types.StreamingRecognitionConfig(config=config)

            print("Oops!  That was no valid number.  Try again...")

            responses = client.streaming_recognize(streaming_config, requests)

            textDict = []

            try:
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

            except:
                print('The last chunk is above 60 seconds.')
        return textDict


    @staticmethod
    def transcribeFromSlicedAudio(configAudio, configSlicing):

        file_name = os.path.join(
            os.path.dirname(__file__),
            'audio', configAudio.filename)

        sound = AudioSegment.from_wav(file_name)

        client = speech.SpeechClient(credentials=Credentials.Credentials.getCredentials())

        chunks = AudioTranscribe.__runSlicing(sound=sound, configSlicing=configSlicing)

        requests = (types.StreamingRecognizeRequest(audio_content=chunk)
                    for chunk in chunks)

        config = types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=configAudio.hertz,
            language_code=configAudio.languageCode,
            enable_word_time_offsets=True)

        streaming_config = types.StreamingRecognitionConfig(config=config)

        print("Oops!  That was no valid number.  Try again...")

        responses = client.streaming_recognize(streaming_config, requests)

        try:
            # Get all responses and words of each response and timespan of each word
            for response in responses:
                for result in response.results:
                    print('Finished: {}'.format(result.is_final))
                    for alternative in result.alternatives:

                        for word_info in alternative.words:
                            word = word_info.word
                            start_time = word_info.start_time
                            end_time = word_info.end_time
                            print('Word: {}, start_time: {}, end_time: {}'.format(word, start_time.seconds, end_time.seconds))

        except:
            print('The last chunk is above 60 seconds.')


    @staticmethod
    def __runSlicing(sound, configSlicing):
        """

        :param sound: The audio file to be sliced
        :param configSlicing: The config for slicing
        :return: list of audio chunks
        """
        times = 1
        tmpStart = 0
        chunks = []

        start = configSlicing.start
        end = configSlicing.end

        while start < (sound.duration_seconds * 1000):

            slicedAudio = AudioTranscribe.__getSlicedAudio(sound,
                                                         start,
                                                         end,
                                                         configSlicing.interval,
                                                         configSlicing.silence_thresh)

            audiochunk = slicedAudio['audiochunk']
            leftpointer = slicedAudio['leftpointer']

            if tmpStart != leftpointer:
                tmpStart = leftpointer
            else:
                times += 1
                if times == 2:
                    return chunks

            start = leftpointer

            end = int((leftpointer + configSlicing.minute) if (leftpointer + configSlicing.minute) < (sound.duration_seconds * 1000) else (
                        sound.duration_seconds * 1000))

            chunks.append(audiochunk.raw_data)


    @staticmethod
    def __getSlicedAudio(sound, start, end, interval, silence_thresh):
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

        print('starttime:{} - endtime:{}'.format(start, end))

        for right in range(end, start, -interval):

            tmpJumpLeft = right-jumptLeft

            audio_slice = sound[tmpJumpLeft: right]

            if audio_slice.dBFS < silence_thresh or audio_slice.dBFS == -float('inf'):
                # print('dBFS:{} - starttime:{} - endtime:{}'.format(audio_slice.dBFS, tmpJumpLeft, right))
                return {'audiochunk': sound[start: tmpJumpLeft], 'leftpointer': tmpJumpLeft}


    @staticmethod
    def __save_in_csv(filename, text):
        with open('textfiles/'+filename+'.csv', 'w') as csvfile:
            fieldnames = ['starttime', 'endtime', 'word']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()

            for x in text:
                for word_info in x.words:
                    word = word_info.word
                    start_time = word_info.start_time
                    end_time = word_info.end_time
                    writer.writerow({'starttime': start_time, 'endtime': end_time, 'word': word})

    @staticmethod
    def __save_in_txt(filename, text):
        with open('textfiles/'+filename+'.txt', 'w') as txtfile:

            for x in text:
                txtfile.write(x.transcript + "\n")