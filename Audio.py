
class Audio:

    filename = ''
    hertz = ''
    languageCode = ''
    fileFormat = ''

    def __init__(self, filename, languageCode, hertz=None, fileFormat=None):
        self.filename = filename
        self.hertz = hertz
        self.languageCode = languageCode
        self.fileFormat = fileFormat