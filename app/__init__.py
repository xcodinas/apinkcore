import logging
import sys

from werkzeug.exceptions import HTTPException

from flask import Flask
from flask_restful import Api as _Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

from config import Config


app = Flask(__name__)
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)


class Api(_Api):
    def error_router(self, original_handler, e):
        if self._has_fr_route() and isinstance(e, HTTPException):
            try:
                return self.handle_error(e)
            except Exception:
                pass
        return original_handler(e)

api = Api(app)
app.config.from_object(Config)
app.secret_key = b'_5#y2L4Q8z\n\xec]/'


db = SQLAlchemy(app)
migrate = Migrate(app, db)

jwt = JWTManager(app)


from app.resources.user import UserResource
from app.resources.device import DeviceResource

# User
api.add_resource(UserResource, '/user')
api.add_resource(DeviceResource, '/device')

from app import routes
from app import utils
from app import exceptions
assert routes
assert utils
assert exceptions
