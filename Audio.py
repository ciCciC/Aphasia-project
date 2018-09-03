
class Audio:

    filename = ''
    hertz = ''
    languageCode = ''
    audioEncoding = 0

    def __init__(self, filename, hertz, languageCode, audioEncoding):
        self.filename = filename
        self.hertz = hertz
        self.languageCode = languageCode
        self.audioEncoding = audioEncoding