import pyaudio
import wave
import time
import os
import io
import math

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
from google.oauth2 import service_account

maybe = (1024+256)**2
CHUNK = 1888152
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 16000
RECORD_SECONDS = 59
WAVE_OUTPUT_FILENAME = "output.wav"
CHUNK_GET = (1888152/RECORD_SECONDS)*20

creds = os.path.join(
    os.path.dirname(__file__),
    'resources',
    'cred.json')

credentials = service_account.Credentials.from_service_account_file(creds)

client = speech.SpeechClient(credentials=credentials)

file_name = "/Users/koray/PycharmProjects/AphasiaProject/audio/billgates.wav"

wf = wave.open(file_name, 'rb')

p = pyaudio.PyAudio()

with io.open(file_name, 'rb') as audio_file:
    content = audio_file.read()

stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)

config = types.RecognitionConfig(
    encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=16000,
    language_code='nl-NL')

streaming_config = types.StreamingRecognitionConfig(config=config, single_utterance=False)

# stream = [content]

print("* recording")

responses = []

count = 0

while count < RECORD_SECONDS:
    data = wf.readframes(int(CHUNK_GET))

    audio = types.RecognitionAudio(content=data)
    operation = client.long_running_recognize(config, audio)
    response = operation.result(timeout=90)
    responses.append(response)
    count += 20
    # time.sleep(20)

for x in responses:
    for result in x.results:
        print(u'Transcript: {}'.format(result.alternatives[0].transcript))

print("* done recording")

stream.stop_stream()
stream.close()
p.terminate()

# wf.setnchannels(CHANNELS)
# wf.setsampwidth(p.get_sample_size(FORMAT))
# wf.setframerate(RATE)
# wf.writeframes(b''.join(frames))
# wf.close()