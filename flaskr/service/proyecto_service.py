from datetime import datetime
import pytz

from flaskr.Entity.dao.proyecto_dao import ProyectoDAO
from flaskr.Entity.dto.proyecto_dto import ProyectoDTO


def obtener_hora_actual():
    zona_horaria = pytz.timezone("America/Bogota") # type: ignore
    return datetime.now(zona_horaria).strftime('%Y-%m-%d %H:%M:%S')

class ProyectoService:
    def __init__(self):
        self.proyecto_dao = ProyectoDAO()

    def insert_proyecto(self, id_usuario: int, id_vista: int, nombre_proyecto: str):
        horario_actual = obtener_hora_actual()

        new_project = ProyectoDTO(
            id_proyecto=0,
            id_usuario=id_usuario,
            id_vista=id_vista,
            nombre_proyecto=nombre_proyecto,
            fecha_creacion=horario_actual,
            fecha_actualizacion=horario_actual,
            fecha_eliminacion=None
        )

        return self.proyecto_dao.insertar_proyecto(new_project)
    
    def actualizar_proyecto(self, id_proyecto, id_usuario=None, id_vista=None, nombre_proyecto=None):
        proyecto = self.proyecto_dao.consultar_proyectoid(id_proyecto)

        if not proyecto:
            return False

        proyecto_data = {
            'id_usuario': id_usuario if id_usuario is not None else proyecto['id_usuario'],
            'id_vista': id_vista if id_vista is not None else proyecto['id_vista'],
            'nombre_proyecto': nombre_proyecto if nombre_proyecto is not None else proyecto['nombre_proyecto'],
            'fecha_creacion': proyecto['fecha_creacion'], 
            'fecha_actualizacion': obtener_hora_actual(),
            'fecha_eliminacion': proyecto['fecha_eliminacion'] if proyecto['fecha_eliminacion'] else None
        }

        return self.proyecto_dao.actualizar_proyecto(ProyectoDTO(id_proyecto=id_proyecto, **proyecto_data))
    
    def borrar_proyecto(self, id_proyecto):
        resultado = self.proyecto_dao.borrar_proyecto(id_proyecto)

        if resultado:
            return {"message": "Proyecto eliminado exitosamente"}, 200
        else:
            return {"error": "No se encontró el proyecto o ya estaba eliminado"}, 400
        
    def listar_proyectos(self):
        projet = self.proyecto_dao.listar_proyectos()
        proyectos = [
            ProyectoDTO(
                id_proyecto=proyecto['id_proyecto'],
                id_usuario=proyecto['id_usuario'],
                id_vista=proyecto['id_vista'],
                nombre_proyecto=proyecto['nombre_proyecto'],
                fecha_creacion=proyecto['fecha_creacion'],
                fecha_actualizacion=proyecto['fecha_actualizacion'],
                fecha_eliminacion=proyecto['fecha_eliminacion']
            ) for proyecto in projet
        ]
        return proyectos