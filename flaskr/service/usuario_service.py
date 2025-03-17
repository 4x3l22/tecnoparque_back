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
