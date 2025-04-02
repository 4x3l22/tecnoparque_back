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

    def actualizar_usuario(self, usuario: UsuarioDTO):
        return self.update('usuario',{
            'nombre': usuario.nombre,
            'correo': usuario.correo,
            'contrasena': usuario.contrasena,
            'fecha_actualizacion': usuario.fecha_actualizacion,
            'fecha_eliminacion': usuario.fecha_eliminacion
        },'id_usuario', usuario.id_usuario)
    
    def borrar_usuario(self, user_id):
        return self.delete('usuario', 'id_usuario', user_id)
    
    def obtener_todos_los_usuarios(self):
        return self.obtener_todos('usuario')

    def obtener_usuario_por_correo(self, correo):
        query = """
            SELECT u.id_usuario, u.contrasena, p.ruta, u.rol
            FROM tecnoparque.usuario u
            LEFT JOIN tecnoparque.proyectos p ON u.id_usuario = p.id_usuario
            WHERE u.correo = %s  
        """
        params = (correo,)

        resultado = self.execute_query(query, params)

        # Verificar si hay resultados y devolver solo el primero
        return resultado[0] if resultado else None
