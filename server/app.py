from flask import Flask
from controllers.mpesa_controllers import mpesa_bp


app = Flask(__name__)

app.register_blueprint(mpesa_bp)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5555, debug=True)