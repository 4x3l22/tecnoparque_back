from werkzeug.security import generate_password_hash, check_password_hash
from flaskr.Entity.dao.usuario_doa import UsuarioDao
from flaskr.Entity.dto.usuario_dto import UsuarioDTO
from datetime import datetime
import pytz

def obtener_hora_actual():
    zona_horaria = pytz.timezone("America/Bogota")
    return datetime.now(zona_horaria).strftime('%Y-%m-%d %H:%M:%S')

class UsuarioService:

    def __init__(self):
        self.usuario_dao = UsuarioDao()

    def insert_usuario(self, nombre: str, correo: str, contrasena: str):
        horario_actual = obtener_hora_actual()

        # Hashear la contraseña
        hashed_password = generate_password_hash(contrasena)

        new_user = UsuarioDTO(
            id_usuario=0,
            nombre=nombre,
            correo=correo,
            contrasena=hashed_password,
            fecha_creacion=horario_actual,
            fecha_actualizacion=horario_actual,
            fecha_eliminacion=None
        )

        return self.usuario_dao.insertar_usuario(new_user)

    def update_user(self, id_usuario, nombre=None, correo=None, contrasena=None):
        usuario = self.usuario_dao.get_userId(id_usuario)
        hashed_password = generate_password_hash(contrasena)

        if not usuario:
            return False

        usuario_data = {
            'nombre': nombre if nombre is not None else usuario['nombre'],
            'correo': correo if correo is not None else usuario['correo'],
            'contrasena': hashed_password if hashed_password is not None else usuario['contrasena'],
            'fecha_creacion': usuario['fecha_creacion'], 
            'fecha_actualizacion': obtener_hora_actual(),
            'fecha_eliminacion': usuario['fecha_eliminacion'] if usuario['fecha_eliminacion'] else None
        }

        return self.usuario_dao.actualizar_usuario(UsuarioDTO(id_usuario=id_usuario, **usuario_data))
    
    def delete_user(self, id_usuario):
        resultado = self.usuario_dao.borrar_usuario(id_usuario)

        if resultado:
            return {"message": "Usuario eliminado exitosamente"}, 200
        else:
            return {"error": "No se encontró el usuario o ya estaba eliminado"}, 400

    def get_all_users(self):
        try:
            users = self.usuario_dao.obtener_todos_los_usuarios()

            users = [
                UsuarioDTO(
                    id_usuario=usuario["id_usuario"],
                    nombre=usuario["nombre"],
                    correo=usuario["correo"],
                    contrasena=usuario["contrasena"],
                    fecha_creacion=usuario["fecha_creacion"],
                    fecha_actualizacion=usuario["fecha_actualizacion"],
                    fecha_eliminacion=usuario["fecha_eliminacion"]
                ) for usuario in users
            ]
            return users
        except Exception as e:
            print("Error en get_all_users:", str(e))
            return {"error": str(e)}, 500

    def login(self, correo: str, contrasena: SyntaxWarning):
        usuario = self.usuario_dao.obtener_usuario_por_correo(correo)

        if not usuario:
            return {"error": "Usuario no encontrado"}, 404

        if not check_password_hash(usuario["contrasena"], contrasena):
            return {"error": "Contraseña incorrecta"}, 400

        return {"message": "Inicio de sesión exitoso"}, 200