from flask_restful import fields


def datetime_to_string(date):
    return date.strftime("%a, %d %b %Y %H:%M:%S -0000")


def non_empty_string(s):
    if not s:
        raise ValueError("Must not be empty string")
    return s

user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'full_name': fields.String,
    'email': fields.String,
}

values_history_fields = {
    'id': fields.Integer,
    'temperature': fields.Float,
    'moisture': fields.Float,
    'measured_at': fields.DateTime,
    'received_at': fields.DateTime,
}

device_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'ip_address': fields.String,
    'mac_address': fields.String,
    'on': fields.Boolean,
}
