import os

from google.cloud import storage

import Credentials
from AudioConverter import AudioConverter


class datastore:

    @staticmethod
    def addAudioFile(source_file_name, fileFormat, destination_blob_name=None):
        """
        :param source_file_name: Enter the name of the file E.G. example, NOT example.mp3
        :param fileFormat: Type extension. E.G. mp3 or wav
        :param destination_blob_name: Enter the name to name the file on storage E.G. exampleBlob
        :return:
        """

        source_corverted_file = AudioConverter.convert_Audio(source_file_name, fileFormat, "flac")

        storage_client = storage.Client(project=Credentials.Credentials.getStorageName(), credentials=Credentials.Credentials.getCredentials())

        bucket = storage_client.get_bucket(Credentials.Credentials.getStorageName())
        blob = bucket.blob(destination_blob_name if destination_blob_name is not None else source_file_name)

        blob.upload_from_filename(source_corverted_file)

        os.remove(source_corverted_file)

        print('File {} uploaded to aphasia-project bucket.'.format(source_file_name))

        pass


    @staticmethod
    def deleteAudioFile(audioName):
        # TODO !
        deleted = True

        return deleted

    @staticmethod
    def list_storage_files():
        """

        :return: A list of files on the storage
        """
        storage_client = storage.Client(project=Credentials.Credentials.getStorageName(), credentials=Credentials.Credentials.getCredentials())
        bucket = storage_client.get_bucket(Credentials.Credentials.getStorageName())

        blobs = bucket.list_blobs()

        for blob in blobs:
            print(blob.name)