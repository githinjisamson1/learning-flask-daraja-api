from flask import Flask
from flask_restful import Api, Resource


app = Flask(__name__)
api = Api(app)


class Index(Resource):
    def get(self):
        return "Hello World", 200


api.add_resource(Index, "/")


if __name__ == "__main__":
    app.run(port=5555, debug=True)
