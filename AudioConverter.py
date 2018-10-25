import glob
import os

from pydub import AudioSegment


class AudioConverter:

    @staticmethod
    def getAudio(filename, fromFormat):
        file_name = os.path.join(
            os.path.dirname(__file__),
            'audio', filename + '.' + fromFormat)

        return file_name

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


    @staticmethod
    def convert_Audio(filename, fromFormat, toFormat):
        """

        :param filename: Only file name! E.G. woord and NOT woord.mp3
        :param fromFormat: Type extension. E.G. mp3 or wav
        :param toFormat: Output extension, it has to be FLAC!!
        :return:
        """

        file_name = os.path.join(
            os.path.dirname(__file__),
            'audiotest', filename + '.' + fromFormat)

        if fromFormat not in ['mp3', 'wav']:
            raise ValueError('Wrong extension! Enter mp3 or wav file.')

        audio = AudioSegment.from_mp3(file_name) if fromFormat == 'mp3' else AudioSegment.from_wav(file_name)

        changedAudio = audio.set_frame_rate(16000).set_channels(1)

        tempPath = os.path.join(os.path.dirname(__file__), 'temp/')

        changedAudio.export(tempPath + filename + '.' + toFormat, format=toFormat)

        return tempPath + filename + '.' + toFormat

    @staticmethod
    def convert_audio_aifc_to_wav(filename, toFormat):
        file_name = os.path.join(
            os.path.dirname(__file__),
            'audio', filename + '.aifc')

        audio = AudioSegment.from_file(file_name, 'aiff')

        changedAudio = audio.set_frame_rate(16000).set_channels(1)

        tempPath = os.path.join(os.path.dirname(__file__), 'temp/')

        changedAudio.export(tempPath + filename + '.' + toFormat, format=toFormat)

        return tempPath + filename + '.' + toFormat
