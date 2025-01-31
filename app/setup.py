from flask import Flask
from flask_restful import Api


def create_app():
    """Create and configure the Flask app."""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'a5e58e67566ab485adc780242b23126b1c9174e0'
    app.config['JWT_ALGORITHM'] = 'HS256'

    return app  # No API creation here
