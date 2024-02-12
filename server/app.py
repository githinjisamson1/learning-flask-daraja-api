from flask import Flask
from flask_restful import Api, Resource
from dotenv import load_dotenv
from os import environ
import requests
from requests.auth import HTTPBasicAuth

load_dotenv()


app = Flask(__name__)
api = Api(app)

# mpesa details
consumer_key = environ.get("CONSUMER_KEY")
consumer_secret = environ.get("CONSUMER_SECRET")


class Index(Resource):
    def get(self):
        return "Hello World", 200

# function to get access_token


def access_token():
    mpesa_auth_url = environ.get("MPESA_AUTH_URL")
    data = requests.get(mpesa_auth_url, auth=HTTPBasicAuth(
        consumer_key, consumer_secret)).json()

    return data


class AccessToken(Resource):
    def get(self):
        data = access_token()

        return data["access_token"]


api.add_resource(Index, "/")
api.add_resource(AccessToken, "/access_token")


if __name__ == "__main__":
    app.run(port=5555, debug=True)
