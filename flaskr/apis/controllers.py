from flask_restful import Resource
from flasgger import Swagger, swag_from
from flask import request

from flaskr.service.sensor_service import FirebaseService

swagger = Swagger()
class SensorController(Resource):
    def __init__(self):
        self.service = FirebaseService()

    @swag_from({
        'tags': ['proceso'],
        'parameters': [
            {
                'name': 'collection',
                'in': 'path',
                'type': 'string',
                'required': True,
                'description': 'Nombre de la colección en Firebase'
            }
        ],
        'responses': {
            200: {
                'description': 'Lista de documentos de la colección',
                'schema': {
                    'type': 'array',
                    'items': {'type': 'object'}
                }
            },
            500: {
                'description': 'Error en el servidor'
            }
        }
    })
    def get(self, collection):
        return self.service.get_sensor_data(collection)

class SensorunoController(Resource):
    def __init__(self):
        self.service = FirebaseService()

    @swag_from({
        'tags': ['proceso'],
        'parameters': [
            {
                'name': 'collection',
                'in': 'path',
                'type': 'string',
                'required': True,
                'description': 'Nombre de la colección en Firebase'
            }
        ],
        'responses': {
            200: {
                'description': 'Lista de documentos de la colección',
                'schema': {
                    'type': 'array',
                    'items': {'type': 'object'}
                }
            },
            500: {
                'description': 'Error en el servidor'
            }
        }
    })
    def get(self, collection):
        return self.service.get_end_rows(collection)
    
class SensorDataController(Resource):
    def __init__(self):
        self.service = FirebaseService()

    @swag_from({
        'tags': ['proceso'],
        'parameters': [
            {
                'name': 'collection',
                'in': 'path',
                'type': 'string',
                'required': True,
                'description': 'Nombre de la colección en Firebase'
            },
            {
                'name': 'start_date',
                'in': 'query',
                'type': 'string',
                'required': True,
                'description': 'Fecha de inicio en formato YYYY-MM-DD'
            },
            {
                'name': 'end_date',
                'in': 'query',
                'type': 'string',
                'required': True,
                'description': 'Fecha de fin en formato YYYY-MM-DD'
            }
        ],
        'responses': {
            200: {
                'description': 'Datos obtenidos exitosamente',
                'schema': {
                    'type': 'array',
                    'items': {'type': 'object'}
                }
            },
            400: {
                'description': 'Solicitud incorrecta'
            },
            500: {
                'description': 'Error en el servidor'
            }
        }
    })
    def get(self, collection):
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        if not start_date or not end_date:
            return {'message': 'start_date and end_date are required'}, 400
        try:
            data = self.service.get_sensor_data_by_date(collection, start_date, end_date)
            return data, 200
        except Exception as e:
            return {'message': str(e)}, 500