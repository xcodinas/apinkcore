import re
from functools import wraps, lru_cache

from sqlalchemy.sql import func
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, \
    verify_jwt_in_request_optional


from app import db, app
from app.models import User


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
