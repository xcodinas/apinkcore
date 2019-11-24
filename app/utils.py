import requests
import re
from functools import wraps, lru_cache

from sqlalchemy.sql import func
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, \
    verify_jwt_in_request_optional


from app import db, app
from app.models import User
from config import Config


TAG_RE = re.compile(r'<[^>]+>')


def needs_user(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request_optional()
        current_user = User.query.filter_by(id=get_jwt_identity()).first()
        if not current_user:
            return
        return func(current_user)
    return wrapper


@app.after_request
def after_request(response):
    # https://stackoverflow.com/questions/30241911/psycopg2-error-databaseerror-error-with-no-message-from-the-libpq
    db.engine.dispose()

    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers',
        'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods',
        'GET,PUT,POST,DELETE')
    return response


def current_user():
    user = User.query.filter_by(id=get_jwt_identity()).first()
    if not user:
        response = {
                'success': 0,
                'error': {
                    'message': 'Unknown user check that auth token is correct',
                }}
        return jsonify(response), 401
    return user


@lru_cache(99999)
def str2bool(v):
    if isinstance(v, bool):
        return
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        return None


def filter_text(text):
    return TAG_RE.sub('', text)


def valid_email(email):
    if re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*'
            + '(\.[a-z]{2,4})$', email) == None:
        return False
    return True


def unaccent_sql(column):
    return func.translate(column, 'áéíóúàèìòùäëïöüâêîôû',
        'aeiouaeiouaeiouaeiou')


def abort(code, json=False, *args, **kwargs):
    response = {
            'success': 0,
            'error': {}}
    response['error'] = kwargs
    return jsonify(response) if json else response, code


class DataInfo:
    def __init__(self, temperature, moisture):
        self.temperature = temperature
        self.moisture = moisture

    def __repr__(self):
        return f"""<DataInfo temperature:{self.temperature}
            moisture:{self.moisture}>"""

    def __str__(self):
        return self._repr_()

    @staticmethod
    def undo_byte_cod(byte):
        return int(byte) - 27

    @staticmethod
    def from_byte_array(byte_arr):
        pre = DataInfo.undo_byte_cod(byte_arr[0])
        post = DataInfo.undo_byte_cod(byte_arr[1])
        moisture = DataInfo.undo_byte_cod(byte_arr[2])
        temperature = float(f'{pre}.{post}')
        return DataInfo(temperature, moisture)


def grouped(iterable, n):
    return zip(*[iter(iterable)] * n)


def recover_data(hex):
    byte_data = bytes.fromhex(hex)
    return list(map(DataInfo.from_byte_array, grouped(byte_data, 3)))


def toggle_switch(name, state):
    if state == 'on':
        requests.post(('https://maker.ifttt.com/trigger/%s_open/with/key' +
            '/%s') % (name, Config.IFTTT))
        return True
    elif state == 'off':
        requests.post(('https://maker.ifttt.com/trigger/%s_close/with/' +
            'key/%s') % (name, Config.IFTTT))
        return False
