

class Store:

    @staticmethod
    def addAudioFile(Audio, bucket_name, source_file_name, destination_blob_name, client):
        """Uploads a file to the bucket."""
        # storage_client = storage.Client()
        #
        # bucket = storage_client.get_bucket(bucket_name)
        # blob = bucket.blob(destination_blob_name)
        #
        # blob.upload_from_filename(source_file_name)
        #
        # print('File {} uploaded to {}.'.format(
        #     source_file_name,
        #     destination_blob_name))
        pass

    @staticmethod
    def getAudioFile():
        audioLink = ''
        return audioLink

    @staticmethod
    def deleteAudioFile(audioName):

        deleted = True

        return deleted