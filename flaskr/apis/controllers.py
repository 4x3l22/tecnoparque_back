from flask_restful import Resource
from flasgger import Swagger, swag_from
from flask import request, jsonify

from flaskr.service import vista_service
from flaskr.service.sensor_service import FirebaseService
from flaskr.service.usuario_service import UsuarioService
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

#Aca estan los controladores de MSQsl
class VistasPostGetController(Resource):
    def __init__(self):
        self.service = VistaService()

    @swag_from({
        'tags': ['Vistas'],
        'summary': 'Registrar una nueva vista',
        'description': 'Este endpoint permite registrar una nueva vista en la base de datos.',
        'parameters': [
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'descripcion': {'type': 'string', 'description': 'Descripción de la vista'},
                        'ruta': {'type': 'string', 'description': 'Ruta de la vista'},
                        'nombre': {'type': 'string', 'description': 'Nombre de la vista'}
                    },
                    'required': ['descripcion', 'ruta', 'nombre']
                }
            }
        ],
        'responses': {
            201: {
                'description': 'Vista creada exitosamente',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'message': {'type': 'string'},
                        'id': {'type': 'integer'}
                    }
                }
            },
            400: {
                'description': 'Solicitud incorrecta - Faltan datos requeridos',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'error': {'type': 'string'}
                    }
                }
            },
            500: {
                'description': 'Error en el servidor',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'error': {'type': 'string'}
                    }
                }
            }
        }
    })
    def post(self):
        """Endpoint para registrar una nueva vista."""
        data = request.get_json()

        if not data or not all(k in data for k in ("descripcion", "ruta", "nombre")):
            return {"error": "Faltan datos requeridos"}, 400

        try:
            vista_id = self.service.registrar_vista(
                descripcion=data["descripcion"],
                ruta=data["ruta"],
                nombre=data["nombre"]
            )
            return {"message": "Vista creada", "id": vista_id}, 201
        except Exception as e:
            return {"error": str(e)}, 500

    @swag_from({
        'tags': ['Vistas'],
        'summary': 'Obtener todas las vistas',
        'description': 'Este endpoint retorna todas las vistas disponibles en la base de datos.',
        'responses': {
            200: {
                'description': 'Lista de vistas obtenida exitosamente',
                'schema': {
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'properties': {
                            'id_vista': {'type': 'integer'},
                            'descripcion': {'type': 'string'},
                            'fecha_creacion': {'type': 'string'},
                            'fecha_actualizacion': {'type': 'string'},
                            'fecha_eliminacion': {'type': 'string'},
                            'ruta': {'type': 'string'},
                            'nombre': {'type': 'string'}
                        }
                    }
                }
            },
            500: {
                'description': 'Error en el servidor',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'error': {'type': 'string'}
                    }
                }
            }
        }
    })
    def get(self):
        """Endpoint para obtener todas las vistas existentes."""
        try:
            vistas = self.service.obtener_todas_las_vistas()
            serialized_vistas = [
                {
                    "id_vista": vista.id_vista,
                    "descripcion": vista.descripcion,
                    "fecha_creacion": vista.fecha_creacion.isoformat() if vista.fecha_creacion else None,
                    "fecha_actualizacion": vista.fecha_actualizacion.isoformat() if vista.fecha_actualizacion else None,
                    "fecha_eliminacion": vista.fecha_eliminacion.isoformat() if vista.fecha_eliminacion else None,
                    "ruta": vista.ruta,
                    "nombre": vista.nombre
                }
                for vista in vistas
            ]
            return serialized_vistas, 200
        except Exception as e:
            return {"error": str(e)}, 500

class VistasPutController(Resource):
    def __init__(self):
        self.service = VistaService()

    @swag_from({
        'tags': ['Vistas'],
        'summary': 'Eliminar una vista',
        'description': 'Este endpoint realiza un borrado lógico marcando la fecha de eliminación en la base de datos.',
        'parameters': [
            {
                'name': 'id_vista',
                'in': 'path',
                'type': 'integer',
                'required': True,
                'description': 'ID de la vista a eliminar'
            }
        ],
        'responses': {
            200: {
                'description': 'Vista eliminada exitosamente',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'message': {'type': 'string'}
                    }
                }
            },
            400: {
                'description': 'Solicitud incorrecta - ID inválido',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'error': {'type': 'string'}
                    }
                }
            },
            500: {
                'description': 'Error en el servidor',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'error': {'type': 'string'}
                    }
                }
            }
        }
    })
    def delete(self, id_vista):
        """Realiza un borrado lógico de una vista."""
        try:
            response, status_code = self.service.borrar_vista(id_vista)
            return response, status_code
        except ValueError as e:
            return {"error": str(e)}, 400
        except Exception as e:
            return {"error": str(e)}, 500

    @swag_from({
        'tags': ['Vistas'],
        'summary': 'Actualizar una vista existente',
        'description': 'Este endpoint actualiza una vista sin modificar la fecha de creación.',
        'parameters': [
            {
                'name': 'id_vista',
                'in': 'path',
                'type': 'integer',
                'required': True,
                'description': 'ID de la vista a actualizar'
            },
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'descripcion': {'type': 'string', 'description': 'Nueva descripción de la vista'},
                        'ruta': {'type': 'string', 'description': 'Nueva ruta de la vista'},
                        'nombre': {'type': 'string', 'description': 'Nuevo nombre de la vista'}
                    }
                }
            }
        ],
        'responses': {
            200: {
                'description': 'Vista actualizada exitosamente',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'message': {'type': 'string'}
                    }
                }
            },
            400: {
                'description': 'Solicitud incorrecta - Faltan datos requeridos',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'error': {'type': 'string'}
                    }
                }
            },
            404: {
                'description': 'Vista no encontrada',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'error': {'type': 'string'}
                    }
                }
            },
            500: {
                'description': 'Error en el servidor',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'error': {'type': 'string'}
                    }
                }
            }
        }
    })
    def put(self, id_vista):
        """Actualiza una vista sin modificar la fecha de creación"""
        data = request.json

        if not data or not any(k in data for k in ("descripcion", "ruta", "nombre")):
            return {"error": "Se requiere al menos un campo para actualizar"}, 400

        try:
            actualizado = self.service.actualizar_vista(
                id_vista=id_vista,
                descripcion=data.get("descripcion"),
                ruta=data.get("ruta"),
                nombre=data.get("nombre")
            )

            if actualizado:  # Ya no intentamos indexar un int
                return {"message": "Vista actualizada exitosamente"}, 200
            else:
                return {"error": "Vista no encontrada"}, 404
        except Exception as e:
            return {"error": str(e)}, 500

class UsuarioPostGetController(Resource):
    def __init__(self):
        self.service = UsuarioService()


    @swag_from({
        'tags': ['Usuario'],
        'summary': 'Registrar un nuevo usuario',
        'description': 'Este endpoint permite registrar un nuevo usuario en la base de datos.',
        'parameters': [
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'nombre': {'type': 'string', 'description': 'Nombre del usuario'},
                        'correo': {'type': 'string', 'description': 'Email del usuario'},
                        'contrasena': {'type': 'string', 'description': '<PASSWORD>'}

                    },
                    'required': ['nombre', 'correo', 'contrasena']
                }
            }
        ],
        'responses': {
            201: {
                'description': 'Usuario creado exitosamente',
            },
            400: {
                'description': 'Solicitud incorrecta - Faltan datos requeridos',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'error': {'type': 'string'}
                    }
                }
            },
            500: {
                'description': 'Error en el servidor',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'error': {'type': 'string'}
                    }
                }
            }
        }
    })
    def post(self):
        """Endpoint para registrar un nuevo usuario."""
        data = request.get_json()

        if not data or not all(k in data for k in ("nombre", "correo", "contrasena")):
            return {"error": "Faltan datos requeridos"}, 400

        try:
            user_id = self.service.insert_usuario(
                nombre=data["nombre"],
                correo=data["correo"],
                contrasena=data["contrasena"]
            )
            return {"message": "usuario register ", "id": user_id}, 201
        except Exception as e:
            return {"error": str(e)}, 500

# class UsuarioPutController(Resource):
