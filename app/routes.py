import datetime
import requests
from flask import jsonify, request
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_restful import reqparse, marshal

from app import app, db
from app.models import User, ValuesHistory, SwitchDevice
from app.fields import user_fields, non_empty_string, values_history_fields
from app.utils import valid_email, abort, recover_data

from config import Config

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


@app.route('/switch/<device>/<state>')
def switch(device, state):
    device = (SwitchDevice.query.filter_by(name=device).first() or
        SwitchDevice.query.filter_by(id=device).first())
    if not device:
        return jsonify('Device not found'), 400
    if state == 'on':
        requests.post(('https://maker.ifttt.com/trigger/%s_open/with/key' +
            '/%s') % (device.name, Config.IFTTT))
        return jsonify('ok'), 200
    elif state == 'off':
        requests.post(('https://maker.ifttt.com/trigger/%s_close/with/' +
            'key/%s') % (device.name, Config.IFTTT))
        return jsonify('ok'), 200


@app.route('/sigfox', methods=['POST'])
def sigfox():
    measurement_time = datetime.datetime.now()
    if request.form.get('time'):
        hour, minute = request.form.get('time').split(':')
        measurement_time = measurement_time.replace(
            hour=int(hour), minute=int(minute))
    if request.form.get('data'):
        values = recover_data(request.form.get('data'))
        for index, value in enumerate(reversed(values)):
            db.session.add(ValuesHistory(
                    measured_at=measurement_time - datetime.timedelta(
                        minutes=(10 / len(values)) * index),
                    moisture=value.moisture,
                    temperature=value.temperature,
                    received_at=datetime.datetime.now()))
        db.session.commit()
    return jsonify('ok'), 200


@app.route('/history')
def history():
    history = ValuesHistory.query.order_by(ValuesHistory.measured_at).all()
    return jsonify(marshal(history, values_history_fields)), 200
