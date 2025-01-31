from .setup import create_app
from flask_restful import Api
import types

def api_route(self, *args, **kwargs):
    """Add endpoint class to the api resource"""

    def wrapper(cls):
        self.add_resource(cls, *args, **kwargs)
        return cls

    return wrapper

app = create_app()
api = Api(app, prefix='/api')  # Create API instance here
api.route = types.MethodType(api_route, api)


from app.api import *

