from ftplib import FTP

from flask import Flask, request
from flask_cors import CORS, cross_origin
from flasgger import Swagger
from werkzeug.utils import secure_filename

from flaskr.apis.urls import api_blueprint
from flaskr.service.proyecto_service import ProyectoService
from flaskr.service.usuario_service import UsuarioService

app = Flask(__name__)

FTP_HOST = "ftp.ingejorgehenao.com"
FTP_USER = "ingejorg"
FTP_PASS = "TOlG51m3.(jF6j"
FTP_FOLDER = "/public_html/bash_img/"

# Extensiones permitidas
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_to_ftp(file):
    """Sube una imagen al servidor FTP y devuelve la URL"""
    filename = secure_filename(file.filename)

    # Conectar al servidor FTP
    with FTP(FTP_HOST) as ftp:
        ftp.login(FTP_USER, FTP_PASS)  # Iniciar sesión
        ftp.cwd(FTP_FOLDER)  # Cambiar al directorio donde queremos subir la imagen

        # Subir la imagen
        ftp.storbinary(f"STOR {filename}", file)

    # Devolver la URL de la imagen
    return f"https://ingejorgehenao.com/bash_img/{filename}"

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
    """Endpoint para registrar un nuevo proyecto con imagen en un servidor FTP."""
    service = ProyectoService()

    if 'img' not in request.files:
        return {"error": "No se envió ninguna imagen"}, 400

    file = request.files['img']
    id_usuario = request.form.get("id_usuario")
    ruta = request.form.get("ruta")
    nombre_proyecto = request.form.get("nombre_proyecto")
    descripcion = request.form.get("descripcion")

    if not id_usuario or not ruta or not nombre_proyecto or not descripcion:
        return {"error": "Faltan datos requeridos"}, 400

    if file and allowed_file(file.filename):
        try:
            img_url = upload_to_ftp(file)  # Subimos la imagen al servidor FTP

            project_id = service.insert_proyecto(
                id_usuario=int(id_usuario),
                ruta=ruta,
                nombre_proyecto=nombre_proyecto,
                descripcion=descripcion,
                img=img_url
            )
            return {"message": "Proyecto creado", "id": project_id, "img_url": img_url}, 201
        except Exception as e:
            return {"error": str(e)}, 500

    return {"error": "Formato de imagen no permitido"}, 400


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
                "img": project.img,
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

@app.route('/usuarios', methods=['GET'])
def usuarios_get():
    """Endpoint para obtener todos los usuarios existentes."""
    service = UsuarioService()
    try:
        users = service.get_all_users()
        serialized_users = [
            {
                "id_usuario": user.id_usuario,
                "nombre": user.nombre
            }
            for user in users
        ]
        return serialized_users, 200
    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == '__main__':
    app.run(debug=True)
