from flask_restful import Resource
from flasgger import Swagger, swag_from
from flask import request

from flaskr.service.sensor_service import FirebaseService
from flaskr.service.vista_service import VistaService

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

class VistaController(Resource):
    def __init__(self):
        self.service = VistaService()

    # POST - Crear una nueva vista
    @swag_from({
        'tags': ['vista'],
        'parameters': [
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'nombre': {'type': 'string'},
                        'descripcion': {'type': 'string'},
                        'ruta': {'type': 'string'},
                        'fecha_creacion': {'type': 'string', 'format': 'date-time'}
                    },
                    'required': ['nombre', 'descripcion', 'ruta', 'fecha_creacion']
                }
            }
        ],
        'responses': {
            201: {
                'description': 'Vista creada exitosamente'
            },
            400: {
                'description': 'Solicitud incorrecta'
            },
            500: {
                'description': 'Error en el servidor'
            }
        }
    })
    def post(self):
        """
        Crear una nueva vista.
        """
        try:
            # Obtenemos los datos del body de la solicitud
            vista_data = request.get_json()
            # Validamos que los campos requeridos existan
            required_fields = ['nombre', 'descripcion', 'ruta', 'fecha_creacion']
            for field in required_fields:
                if field not in vista_data:
                    return {'message': f'El campo {field} es requerido'}, 400

            # Llamamos al servicio para insertar la vista
            self.service.insert_vista((
                vista_data['nombre'],
                vista_data['descripcion'],
                vista_data['ruta'],
                vista_data['fecha_creacion']
            ))
            return {'message': 'Vista creada exitosamente'}, 201
        except Exception as e:
            return {'message': str(e)}, 500

    # PUT - Actualizar una vista existente
    @swag_from({
        'tags': ['vista'],
        'parameters': [
            {
                'name': 'vista_id',
                'in': 'path',
                'type': 'integer',
                'required': True,
                'description': 'ID único de la vista'
            },
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'nombre': {'type': 'string'},
                        'descripcion': {'type': 'string'},
                        'ruta': {'type': 'string'},
                        'fecha_creacion': {'type': 'string', 'format': 'date-time'}
                    }
                }
            }
        ],
        'responses': {
            200: {
                'description': 'Vista actualizada exitosamente'
            },
            400: {
                'description': 'Solicitud incorrecta'
            },
            404: {
                'description': 'Vista no encontrada'
            },
            500: {
                'description': 'Error en el servidor'
            }
        }
    })
    def put(self, vista_id):
        """
        Actualizar una vista existente.
        """
        try:
            # Obtenemos los datos del body de la solicitud
            vista_data = request.get_json()

            # Llamamos al servicio para actualizar los datos de la vista
            self.service.update_vista(vista_id, vista_data)
            return {'message': 'Vista actualizada exitosamente'}, 200
        except Exception as e:
            return {'message': str(e)}, 500

