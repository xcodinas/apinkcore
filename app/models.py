import datetime
from passlib.hash import pbkdf2_sha256 as sha256
from sqlalchemy import event


from app import db


class TimestampsMixin(object):
    created_at = db.Column(db.DateTime,
        default=datetime.datetime.now())
    updated_at = db.Column(db.DateTime,
        default=datetime.datetime.now())

    @staticmethod
    def create_time(mapper, connection, target):
        target.created_at = datetime.datetime.now()

    @staticmethod
    def update_time(mapper, connection, target):
        target.updated_at = datetime.datetime.now()

    @classmethod
    def register(cls):
        event.listen(cls, 'before_insert', cls.create_time)
        event.listen(cls, 'before_update', cls.update_time)


class User(db.Model, TimestampsMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String, nullable=False)
    full_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)


class ValuesHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    received_at = db.Column(db.DateTime,
        default=datetime.datetime.now())
    measured_at = db.Column(db.DateTime)
    temperature = db.Column(db.Float)
    moisture = db.Column(db.Float)


class SwitchDevice(db.Model, TimestampsMixin):
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String, nullable=False)
    mac_address = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    on = db.Column(db.Boolean, default=False)

User.register()
