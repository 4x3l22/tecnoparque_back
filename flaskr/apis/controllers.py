from flask_restful import Resource
from flasgger import Swagger, swag_from
from flask import request, jsonify

from flaskr.service import vista_service
from flaskr.service.proyecto_service import ProyectoService
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
        
    @swag_from({
        'tags': ['Usuario'],
        'summary': 'Obtener todos los usuarios',
        'description': 'Este endpoint retorna todos los usuarios disponibles en la base de datos.',
        'responses': {
            200: {
                'description': 'Lista de usuarios obtenida exitosamente',
                'schema': {
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'properties': {
                            'id_usuario': {'type': 'integer'},
                            'nombre': {'type': 'string'},
                            'correo': {'type': 'string'},
                            'fecha_creacion': {'type': 'string'},
                            'fecha_actualizacion': {'type': 'string'},
                            'fecha_eliminacion': {'type': 'string'}
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
        """Endpoint para obtener todos los usuarios existentes."""
        try:
            users = self.service.get_all_users()
            serialized_users = [
                {
                    "id_usuario": user.id_usuario,
                    "nombre": user.nombre,
                    "correo": user.correo,
                    "fecha_creacion": user.fecha_creacion.isoformat() if user.fecha_creacion else None,
                    "fecha_actualizacion": user.fecha_actualizacion.isoformat() if user.fecha_actualizacion else None,
                    "fecha_eliminacion": user.fecha_eliminacion.isoformat() if user.fecha_eliminacion else None
                }
                for user in users
            ]
            return serialized_users, 200
        except Exception as e:
            return {"error": str(e)}, 500
        
    
        
class UsuarioLoginController(Resource):
    def __init__(self):
        self.service = UsuarioService()

    @swag_from({
        'tags': ['Usuario'],
        'summary': 'iniciar sesion',
        'description': 'Este endpoint permite iniciar sesion en la base de datos.',
        'parameters': [
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'correo': {'type': 'string', 'description': 'Email del usuario'},
                        'contrasena': {'type': 'string', 'description': '<PASSWORD>'}

                    },
                    'required': ['correo', 'contrasena']
                }
            }
        ],
        'responses': {
            200: {
                'description': 'ok',
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
        """Endpoint para iniciar sesion."""
        data = request.get_json()

        if not data or not all(k in data for k in ("correo", "contrasena")):
            return {"error": "Faltan datos requeridos"}, 400

        try:
            user_id = self.service.login(
                correo=data["correo"],
                contrasena=data["contrasena"]
            )
            return {"message": "usuario login ", "id": user_id}, 200
        except Exception as e:
            return {"error": str(e)}, 500

class UsuarioPutController(Resource):

    def __init__(self):
        self.service = UsuarioService()

    @swag_from({
        'tags': ['Usuario'],
        'summary': 'Actualizar un usuario existente',
        'description': 'Este endpoint permite actualizar los datos de un usuario existente.',
        'parameters': [
            {
                'name': 'id_usuario',
                'in': 'path',
                'type': 'integer',
                'required': True,
                'description': 'ID del usuario a actualizar'
            },
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'nombre': {'type': 'string', 'description': 'Nuevo nombre del usuario'},
                        'correo': {'type': 'string', 'description': 'Nuevo correo del usuario'},
                        'contrasena': {'type': 'string', 'description': 'Nueva contraseña del usuario'}
                    }
                }
            }
        ],
        'responses': {
            200: {
                'description': 'Usuario actualizado exitosamente',
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
                'description': 'Usuario no encontrado',
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
    def put(self, id_usuario):
        """Endpoint para actualizar un usuario existente."""
        data = request.get_json()

        if not data or not any(k in data for k in ("nombre", "correo", "contrasena")):
            return {"error": "Se requiere al menos un campo para actualizar"}, 400

        try:
            actualizado = self.service.update_user(
                id_usuario=id_usuario,
                nombre=data.get("nombre"),
                correo=data.get("correo"),
                contrasena=data.get("contrasena")
            )

            if actualizado:
                return {"message": "Usuario actualizado exitosamente"}, 200
            else:
                return {"error": "Usuario no encontrado"}, 404
        except Exception as e:
            return {"error": str(e)}, 500

    @swag_from({
        'tags': ['Usuario'],
        'summary': 'Eliminar un usuario',
        'description': 'Este endpoint realiza un borrado lógico marcando la fecha de eliminación en la base de datos.',
        'parameters': [
            {
                'name': 'id_usuario',
                'in': 'path',
                'type': 'integer',
                'required': True,
                'description': 'ID del usuario a eliminar'
            }
        ],
        'responses': {
            200: {
                'description': 'Usuario eliminado exitosamente',
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
    def delete(self, id_usuario):
        """Realiza un borrado lógico de un usuario."""
        try:
            response, status_code = self.service.delete_user(id_usuario)
            return response, status_code
        except ValueError as e:
            return {"error": str(e)}, 400
        except Exception as e:
            return {"error": str(e)}, 500
        
class ProyectoPostGetController(Resource):

    def __init__(self):
        self.service = ProyectoService()
        
    @swag_from({
        'tags': ['Proyecto'],
        'summary': 'Registrar un nuevo proyecto',
        'description': 'Este endpoint permite registrar un nuevo proyecto en la base de datos.',
        'parameters': [
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'id_usuario': {'type': 'integer', 'description': 'ID del usuario'},
                        'id_vista': {'type': 'integer', 'description': 'ID de la vista'},
                        'nombre_proyecto': {'type': 'string', 'description': 'Nombre del proyecto'}
                    },
                    'required': ['id_usuario', 'id_vista', 'nombre_proyecto']
                }
            }
        ],
        'responses': {
            201: {
                'description': 'Proyecto creado exitosamente',
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
        """Endpoint para registrar un nuevo proyecto."""
        data = request.get_json()

        if not data or not all(k in data for k in ("id_usuario", "id_vista", "nombre_proyecto")):
            return {"error": "Faltan datos requeridos"}, 400

        try:
            project_id = self.service.insert_proyecto(
                id_usuario=data["id_usuario"],
                id_vista=data["id_vista"],
                nombre_proyecto=data["nombre_proyecto"]
            )
            return {"message": "Proyecto creado", "id": project_id}, 201
        except Exception as e:
            return {"error": str(e)}, 500
        
    @swag_from({
        'tags': ['Proyecto'],
        'summary': 'Obtener todos los proyectos',
        'description': 'Este endpoint retorna todos los proyectos disponibles en la base de datos.',
        'responses': {
            200: {
                'description': 'Lista de proyectos obtenida exitosamente',
                'schema': {
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'properties': {
                            'id_proyecto': {'type': 'integer'},
                            'id_usuario': {'type': 'integer'},
                            'id_vista': {'type': 'integer'},
                            'nombre_proyecto': {'type': 'string'},
                            'fecha_creacion': {'type': 'string'},
                            'fecha_actualizacion': {'type': 'string'},
                            'fecha_eliminacion': {'type': 'string'}
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
        """Endpoint para obtener todos los proyectos existentes."""
        try:
            projects = self.service.listar_proyectos()
            serialized_projects = [
                {
                    "id_proyecto": project.id_proyecto,
                    "id_usuario": project.id_usuario,
                    "id_vista": project.id_vista,
                    "nombre_proyecto": project.nombre_proyecto,
                    "fecha_creacion": project.fecha_creacion.isoformat() if project.fecha_creacion else None,
                    "fecha_actualizacion": project.fecha_actualizacion.isoformat() if project.fecha_actualizacion else None,
                    "fecha_eliminacion": project.fecha_eliminacion.isoformat() if project.fecha_eliminacion else None
                }
                for project in projects
            ]
            return serialized_projects, 200
        except Exception as e:
            return {"error": str(e)}, 500
        
class ProyectoPutDeleteController(Resource):
    def __init__(self):
        self.service = ProyectoService()

    @swag_from({
        'tags': ['Proyecto'],
        'summary': 'Actualizar un proyecto existente',
        'description': 'Este endpoint permite actualizar los datos de un proyecto existente.',
        'parameters': [
            {
                'name': 'id_proyecto',
                'in': 'path',
                'type': 'integer',
                'required': True,
                'description': 'ID del proyecto a actualizar'
            },
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'schema': {
                    'type': 'object',
                    'properties': {
                        'id_usuario': {'type': 'integer', 'description': 'Nuevo ID del usuario'},
                        'id_vista': {'type': 'integer', 'description': 'Nuevo ID de la vista'},
                        'nombre_proyecto': {'type': 'string', 'description': 'Nuevo nombre del proyecto'}
                    }
                }
            }
        ],
        'responses': {
            200: {
                'description': 'Proyecto actualizado exitosamente',
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
                'description': 'Proyecto no encontrado',
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
    def put(self, id_proyecto):
        """Endpoint para actualizar un proyecto existente."""
        data = request.get_json()

        if not data or not any(k in data for k in ("id_usuario", "id_vista", "nombre_proyecto")):
            return {"error": "Se requiere al menos un campo para actualizar"}, 400

        try:
            actualizado = self.service.actualizar_proyecto(
                id_proyecto=id_proyecto,
                id_usuario=data.get("id_usuario"),
                id_vista=data.get("id_vista"),
                nombre_proyecto=data.get("nombre_proyecto")
            )

            if actualizado:
                return {"message": "Proyecto actualizado exitosamente"}, 200
            else:
                return {"error": "Proyecto no encontrado"}, 404
        except Exception as e:
            return {"error": str(e)}, 500
        
    @swag_from({
        'tags': ['Proyecto'],
        'summary': 'Eliminar un proyecto',
        'description': 'Este endpoint realiza un borrado lógico marcando la fecha de eliminación en la base de datos.',
        'parameters': [
            {
                'name': 'id_proyecto',
                'in': 'path',
                'type': 'integer',
                'required': True,
                'description': 'ID del proyecto a eliminar'
            }
        ],
        'responses': {
            200: {
                'description': 'Proyecto eliminado exitosamente',
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
    def delete(self, id_proyecto):
        """Realiza un borrado lógico de un proyecto."""
        try:
            response, status_code = self.service.borrar_proyecto(id_proyecto)
            return response, status_code
        except ValueError as e:
            return {"error": str(e)}, 400
        except Exception as e:
            return {"error": str(e)}, 500