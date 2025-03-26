from flaskr.Entity.dao.base_dao import BaseRepository
from flaskr.Entity.dto.proyecto_dto import ProyectoDTO


class ProyectoDAO(BaseRepository):

    def insertar_proyecto(self, proyecto: ProyectoDTO):
        columns = [
            'id_usuario',
            'id_vista',
            'nombre_proyecto',
            'fecha_creacion',
            'fecha_actualizacion',
            'fecha_eliminacion'
        ]
        values = (
            proyecto.id_usuario,
            proyecto.id_vista,
            proyecto.nombre_proyecto,
            proyecto.fecha_creacion,
            proyecto.fecha_actualizacion,
            proyecto.fecha_eliminacion
        )
        return self.insert('proyectos',columns, values)
    
    def consultar_proyectoid(self, proyecto_id):
        return self.obtener_por_id('proyectos','id_proyecto',proyecto_id)
    
    def actualizar_proyecto(self, proyecto: ProyectoDTO):
        return self.update('proyectos',{
            'id_usuario': proyecto.id_usuario,
            'id_vista': proyecto.id_vista,
            'nombre_proyecto': proyecto.nombre_proyecto,
            'fecha_actualizacion': proyecto.fecha_actualizacion,
            'fecha_eliminacion': proyecto.fecha_eliminacion
        },'id_proyecto', proyecto.id_proyecto)
    
    def borrar_proyecto(self, proyecto_id):
        return self.delete('proyectos', 'id_proyecto', proyecto_id)
    
    def listar_proyectos(self):
        return self.obtener_todos('proyectos')