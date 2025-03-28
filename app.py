from flask import Flask, request
from flask_cors import CORS, cross_origin
from flasgger import Swagger
from flaskr.apis.urls import api_blueprint
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
        user_id = service.login(
            correo=data["correo"],
            contrasena=data["contrasena"]
        )
        return {"message": "Usuario autenticado", "ok": user_id}, 200
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

if __name__ == '__main__':
    app.run(debug=True)
