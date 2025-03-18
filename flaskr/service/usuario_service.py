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

        new_user = UsuarioDTO(
            id_usuario=0,
            nombre=nombre,
            correo=correo,
            contrasena=contrasena,
            fecha_creacion=horario_actual,
            fecha_actualizacion=horario_actual,
            fecha_eliminacion=None
        )

        return self.usuario_dao.insertar_usuario(new_user)

    def update_user(self, id_usuario, nombre=None, correo=None, contrasena=None):
        usuario = self.usuario_dao.get_userId(id_usuario)

        if not usuario:
            return False

        usuario_data = {
            'nombre': nombre if nombre is not None else usuario['nombre'],
            'correo': correo if correo is not None else usuario['correo'],
            'contrasena': contrasena if contrasena is not None else usuario['contrasena'],
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
            users = self.usuario_dao.get_all()
            print("Usuarios obtenidos:", users)  # 👀 Ver qué datos devuelve el DAO

            users = [
                UsuarioDTO(
                    id_usuario=usuario[0],
                    nombre=usuario[1],
                    correo=usuario[2],
                    contrasena=usuario[3],
                    fecha_creacion=usuario[4],
                    fecha_actualizacion=usuario[5],
                    fecha_eliminacion=usuario[6]
                ) for usuario in users
            ]
            return users
        except Exception as e:
            print("Error en get_all_users:", str(e))  # 🔍 Imprimir el error exacto
            raise
