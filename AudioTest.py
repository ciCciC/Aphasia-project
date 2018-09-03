import io
import os
import _thread
import time
import math
import itertools
import wave

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
from google.oauth2 import service_account

import Credentials

credentials = service_account.Credentials.from_service_account_file(Credentials.Credentials.cred())

client = speech.SpeechClient(credentials=credentials)

file_name = os.path.join(
    os.path.dirname(__file__),
    'audio',
    'aphasiapatientW.wav')

textfilesPath = os.path.join(
    os.path.dirname(__file__),
    'textfiles',
    'nice.txt')

# config = types.RecognitionConfig(
#     encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
#     sample_rate_hertz=16000,
#     language_code='en-US')

def writeTranscript(responses, writer):
    for response in responses:
        for result in response.results:
            print('Finished: {}'.format(result.is_final))
            for alternative in result.alternatives:
                print(u'Transcript: {}'.format(alternative.transcript))
                writer.write(alternative.transcript + '\n')

f = wave.open(file_name,'r')
frames = f.getnframes()
rate = f.getframerate()
duration = frames / float(rate)

with io.open(file_name, 'rb') as audio_file:
    with open(textfilesPath, 'w') as text_w:
        contentSize = os.path.getsize(file_name)
        CHUNK_MEMORY = (contentSize / duration) * 30
        count = 0
        amountCount = 0


        chuncks = []

        while count < duration:
            chuncks.append(audio_file.read(int(CHUNK_MEMORY)))

            amountCount += 1
            count += 30

        requests = (types.StreamingRecognizeRequest(audio_content=chunk)
                    for chunk in chuncks)

        config = types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code='en-GB')

        streaming_config = types.StreamingRecognitionConfig(config=config)

        responses = client.streaming_recognize(streaming_config, requests)

        writeTranscript(responses, text_w)

# def runThreads(youtube, args, times, delay):
#     count = 0
#
#     while count < times :
#         time.sleep(delay)
#         count += 1
#
#         for i in range(0, count):
#             args.text += "*"
#
#         try:
#             # video_comment_threads = get_comment_threads(youtube, args.videoid)
#             # parent_id = video_comment_threads[0]["id"]
#             insert_commentThread(youtube, args.channelid, args.videoid, args.text)
#             # video_comments = get_comments(youtube, parent_id)
#             print("%s: %s" % (args.text, count))
#
#         except HttpError as e:
#             print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
#         else:
#             print("Inserted, listed, updated, moderated, marked and deleted comments.")