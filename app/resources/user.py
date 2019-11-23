from flask_restful import Resource, reqparse, marshal_with
from flask_jwt_extended import jwt_required

from app.models import User
from app.fields import user_fields


user_parser = reqparse.RequestParser()
user_parser.add_argument('user', type=int)


class UserResource(Resource):

    decorators = [jwt_required]

    @marshal_with(user_fields)
    def get(self):
        args = user_parser.parse_args()
        if not args.user:
            users = User.query.all()
            return users
        return User.query.filter_by(id=args.user).first()
