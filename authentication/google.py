from google.auth.transport import requests
from google.oauth2 import id_token
from rest_framework import serializers

class Google:
    @staticmethod
    def validate(auth_token):
        try:
            idInfo = id_token.verify_oauth2_token(auth_token, requests.Request())
            if "accounts.google.com" in idInfo["iss"]:
                return idInfo
        except:
            raise serializers.ValidationError("The Token is invalid or has expired")
