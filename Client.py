from chardet import enums

import AudioTranscribe
from Audio import Audio

print(AudioTranscribe.fromGoogleStorage(Audio('aphasiapatient.flac', 16000, 'en-GB', enums.RecognitionConfig.AudioEncoding.FLAC)))

AudioTranscribe.fromAudioFile(Audio('aphasiapatientW.wav', 16000, 'en-GB', enums.RecognitionConfig.AudioEncoding.LINEAR16))

# TESSSSST