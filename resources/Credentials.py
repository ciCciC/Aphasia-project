import os
from google.oauth2 import service_account

class Credentials:

    @staticmethod
    def getCredentials():
        return service_account.Credentials.from_service_account_file(Credentials.SERVICECREDENTIALS())

    @staticmethod
    def SERVICECREDENTIALS():
        return os.path.join(
            os.path.dirname(__file__),'audiototext-c92821bf0af8.json')

    @staticmethod
    def cred():
        return os.path.join(
            os.path.dirname(__file__),'cred.json')

    @staticmethod
    def API_KEY_ONLINECONVERTER():
        """
        API of online_converter.com
        :return: API KEY
        """
        return "df8fa8d3e638082ab09fd6147cbfaef1"