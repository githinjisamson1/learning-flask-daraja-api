from flask import Flask
from flask_restful import Api, Resource
from dotenv import load_dotenv
from os import environ

load_dotenv()


app = Flask(__name__)
api = Api(app)

# mpesa details
consumer_key = environ.get("CONSUMER_KEY")
consumer_secret = environ.get("CONSUMER_SECRET")


class Index(Resource):
    def get(self):
        return "Hello World", 200


api.add_resource(Index, "/")


if __name__ == "__main__":
    app.run(port=5555, debug=True)
