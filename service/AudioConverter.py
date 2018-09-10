import glob
import os

class AudioConverter:

    @staticmethod
    def getAudioFiles(fileExtension='*'):
        """
        :param fileExtension: default = *, this takes all extensions in de folder. Enter mp3, wav, flac
        :return: list of audio files
        """
        return glob.glob(os.path.join(
            os.path.dirname(__file__), 'audio/', '*.' + fileExtension))


    @staticmethod
    def exportAudio(audio, fileName, format, filepath=None):
        """
        :param audio: The audio file to be converted
        :param fileName: Give a new file name
        :param format: Specify the extension to which the is to be converted.
        :param filepath: None for default audio folder path. If not None than give the path to export
        """

        if filepath is None:
            filepath = glob.glob(os.path.join(
                os.path.dirname(__file__), 'audio/'))

        if filepath[-1] != '/':
            raise ValueError('Forgot to add /')

        audio.export(filepath + fileName + '.' + format, format=format)

        pass