from flask import jsonify
from flask_restful import Resource, reqparse, marshal_with, marshal

from app import db
from app.models import SwitchDevice
from app.fields import device_fields, non_empty_string
from app.utils import str2bool


filter_device_parser = reqparse.RequestParser()
filter_device_parser.add_argument('device', type=int)

device_parser = reqparse.RequestParser()
device_parser.add_argument('ip_address', type=non_empty_string)
device_parser.add_argument('mac_address', type=non_empty_string)
device_parser.add_argument('name', type=non_empty_string)
device_parser.add_argument('on', type=str2bool)
device_parser.add_argument('id', type=int)


class DeviceResource(Resource):

    @marshal_with(device_fields)
    def get(self):
        args = filter_device_parser.parse_args()
        if not args.device:
            return SwitchDevice.query.all()
        return SwitchDevice.query.filter_by(id=args.device).first()

    def post(self):
        args = device_parser.parse_args()
        if SwitchDevice.query.filter_by(name=args.name).first():
            return jsonify('A device already exists with that name.')
        device = SwitchDevice(
            ip_address=args.ip_address,
            mac_address=args.mac_address,
            name=args.name,
            on=args.on)
        db.session.add(device)
        db.session.commit()
        return jsonify(marshal(device, device_fields))

    @marshal_with(device_fields)
    def put(self):
        args = device_parser.parse_args()
        if args.id:
            device = SwitchDevice.query.filter_by(id=args.id).first()
        else:
            device = SwitchDevice.query.filter_by(name=args.name).first()
        print(device)
        if not device:
            return False
        device.on = args.on if args.on else device.on
        device.name = args.name if args.name else device.name
        device.ip_address = (
            args.ip_address if args.ip_address else device.ip_address)
        device.mac_address = (
            args.mac_address if args.mac_address else device.mac_address)
        db.session.commit()
        return device
