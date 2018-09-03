import io
import os
import _thread
import time

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
from google.oauth2 import service_account

get = os.path.join(
    os.path.dirname(__file__),
    'test',
    'cred.json')

credentials = service_account.Credentials.from_service_account_file(get)

client = speech.SpeechClient(credentials=credentials)

file_name = os.path.join(
    os.path.dirname(__file__),
    'video',
    'woord.mp4')

with io.open(file_name, 'rb') as audio_file:
    content = audio_file.read()

stream = [content]

requests = (types.StreamingRecognizeRequest(audio_content=chunk)
                for chunk in stream)

config = types.RecognitionConfig(
    encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=16000,
    language_code='nl-NL')

streaming_config = types.StreamingRecognitionConfig(config=config, single_utterance=False)

responses = client.streaming_recognize(streaming_config, requests)

for response in responses:
        for result in response.results:
            print('Finished: {}'.format(result.is_final))
            # print('Stability: {}'.format(result.stability))
            alternatives = result.alternatives
            for alternative in alternatives:
                print('Confidence: {}'.format(alternative.confidence))
                print(u'Transcript: {}'.format(alternative.transcript))


