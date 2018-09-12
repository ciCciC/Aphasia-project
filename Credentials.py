import os

from google.oauth2 import service_account

class Credentials:

    @staticmethod
    def getStorageName():
        return 'aphasia-project'

    @staticmethod
    def getCredentials():
        return service_account.Credentials.from_service_account_file(Credentials.__serviceCredentials())

    @staticmethod
    def __serviceCredentials():
        return os.path.join(os.path.dirname(__file__),'resources','audiototext-c92821bf0af8.json')

    @staticmethod
    def cred():
        return os.path.join(os.path.dirname(__file__), 'resources', 'cred.json')