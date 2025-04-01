from flask import Flask, request
from flask_cors import CORS, cross_origin
from flasgger import Swagger
from flaskr.apis.urls import api_blueprint
from flaskr.service.proyecto_service import ProyectoService
from flaskr.service.usuario_service import UsuarioService

app = Flask(__name__)

# Configurar CORS para permitir solicitudes desde cualquier origen
CORS(app)

swagger = Swagger(app)

# 🔹 Registrar los Blueprints
app.register_blueprint(api_blueprint, url_prefix='/api')

@cross_origin
@app.route('/login', methods=['POST'])
def login():
    """Endpoint para iniciar sesión."""
    service = UsuarioService()
    data = request.get_json()

    # Validar datos requeridos
    if not data or not all(key in data for key in ("correo", "contrasena")):
        return {"error": "Faltan datos requeridos"}, 400

    try:
        return service.login(
            correo=data["correo"],
            contrasena=data["contrasena"]
        )

    except Exception as e:
        return {"error": str(e)}, 500
@app.route('/register', methods=['POST'])
def register():
    """Endpoint para registrar un nuevo usuario."""
    service = UsuarioService()
    data = request.get_json()

    if not data or not all(k in data for k in ("nombre", "correo", "contrasena")):
        return {"error": "Faltan datos requeridos"}, 400

    try:
        user_id = service.insert_usuario(
            nombre=data["nombre"],
            correo=data["correo"],
            contrasena=data["contrasena"]
        )
        return {"message": "usuario register ", "id": user_id}, 201
    except Exception as e:
        return {"error": str(e)}, 500

@app.route('/proyecto', methods=['POST'])
def proyecto():
    """Endpoint para registrar un nuevo proyecto."""
    data = request.get_json()
    service = ProyectoService()

    if not data or not all(k in data for k in ("id_usuario", "ruta", "nombre_proyecto")):
        return {"error": "Faltan datos requeridos"}, 400

    try:
        project_id = service.insert_proyecto(
            id_usuario=data["id_usuario"],
            ruta=data["ruta"],
            nombre_proyecto=data["nombre_proyecto"],
            descripcion=data["descripcion"]
        )
        return {"message": "Proyecto creado", "id": project_id}, 201
    except Exception as e:
        return {"error": str(e)}, 500

@app.route('/proyectos', methods=['GET'])
def proyectos_get():
    """Endpoint para obtener todos los proyectos existentes."""
    service = ProyectoService()
    try:
        projects = service.listar_proyectos()
        serialized_projects = [
            {
                "id_proyecto": project.id_proyecto,
                "id_usuario": project.id_usuario,
                "ruta": project.ruta,
                "descripcion": project.descripcion,
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

if __name__ == '__main__':
    app.run(debug=True)
