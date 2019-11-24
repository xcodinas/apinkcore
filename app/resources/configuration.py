from flask import jsonify
from flask_restful import Resource, reqparse, marshal_with, marshal

from app import db
from app.models import Configuration
from app.fields import configuration_fields, non_empty_string


filter_configuration_parser = reqparse.RequestParser()
filter_configuration_parser.add_argument('name', type=str)

configuration_parser = reqparse.RequestParser()
configuration_parser.add_argument('name', type=non_empty_string)
configuration_parser.add_argument('value', type=non_empty_string)


class ConfigurationResource(Resource):

    @marshal_with(configuration_fields)
    def get(self):
        args = filter_configuration_parser.parse_args()
        if not args.name:
            return Configuration.query.all()
        return Configuration.query.filter_by(name=args.name).first()

    def post(self):
        args = configuration_parser.parse_args()
        if Configuration.query.filter_by(name=args.name).first():
            return jsonify('A configuration already exists with that name.')
        configuration = Configuration(
            name=args.name,
            value=args.value,
            )
        db.session.add(configuration)
        db.session.commit()
        return jsonify(marshal(configuration, configuration_fields))

    @marshal_with(configuration_fields)
    def put(self):
        args = configuration_parser.parse_args()
        configuration = Configuration.query.filter_by(name=args.name).first()
        if not configuration:
            return False
        configuration.value = (
            args.value if args.value != None else configuration.value)
        db.session.commit()
        return configuration
