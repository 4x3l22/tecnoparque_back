from flaskr.Entity.dao.base_dao import BaseRepository
from flaskr.Entity.dto.usuario_dto import UsuarioDTO


class UsuarioDao(BaseRepository):

    def insertar_usuario(self, usuario: UsuarioDTO):
        columns = [
            'nombre',
            'correo',
            'contrasena',
            'fecha_creacion',
            'fecha_actualizacion',
            'fecha_eliminacion'
        ]
        values = (
            usuario.nombre,
            usuario.correo,
            usuario.contrasena,
            usuario.fecha_creacion,
            usuario.fecha_actualizacion,
            usuario.fecha_eliminacion
        )
        return self.insert('usuario',columns, values)

    def get_userId(self, user_id):
        return self.obtener_por_id('usuario','id_usuario',user_id)

    