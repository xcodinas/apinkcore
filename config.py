import os
import datetime

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATION = False
    TOKEN_EXPIRATION_SECONDS = 3600
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=7)
    JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(days=30)
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    JWT_SECRET_KEY = 'apinkcore'
    JSON_SORT_KEYS = False
    IFTTT = 'dMdDr_P-TtKvJYRlNXU-bP'
