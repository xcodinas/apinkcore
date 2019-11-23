from flask import jsonify
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_restful import reqparse, marshal

from app import app, db
from app.models import User
from app.fields import user_fields, non_empty_string
from app.utils import valid_email, abort

register_parser = reqparse.RequestParser()
register_parser.add_argument('email', type=non_empty_string, required=True,
help="Email cannot be blank!", trim=True)
register_parser.add_argument('username', type=non_empty_string, required=True,
help="Username cannot be blank!", trim=True)
register_parser.add_argument('password', type=non_empty_string, required=True,
help="Password cannot be blank!", trim=True)
register_parser.add_argument('name', type=non_empty_string, required=True,
help="Name cannot be blank!", trim=True)
register_parser.add_argument('code', type=non_empty_string, required=True,
help="Code cannot be blank!", trim=True)


login_parser = reqparse.RequestParser()
login_parser.add_argument('username', required=True,
help="Username cannot be blank!")
login_parser.add_argument('password', required=True,
help="Password cannot be blank!")


@app.route('/status', methods=['GET'])
@app.route('/', methods=['GET'])
def index():
    return jsonify({}), 200


@app.route('/login', methods=['POST'])
def login():
    args = login_parser.parse_args()
    user = User.query.filter_by(username=args.username).first()
    if not user or not User.verify_hash(args.password, user.password):
        return abort(400, message="Bad username or password")

    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    return jsonify(
        user=marshal(user, user_fields),
        access_token=access_token,
        refresh_token=refresh_token), 200


@app.route('/register', methods=['POST'])
def register():
    args = register_parser.parse_args()
    if User.query.filter(User.username == args.username).count() != 0:
        return abort(400, message={'username': 'Username already registered'})
    elif User.query.filter(User.email == args.email).count() != 0:
        return abort(400, message={'email': 'Email already registered'})
    elif valid_email(args.email) is False:
        return abort(400, message={'email': 'This email is not valid'})

    user = User(
        username=args.username,
        full_name=args.name,
        password=User.generate_hash(args.password),
        email=args.email
        )
    db.session.add(user)
    db.session.commit()
    return jsonify(marshal(user, user_fields))
