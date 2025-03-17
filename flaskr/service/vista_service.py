from datetime import datetime

from sqlalchemy import null

from flaskr.Entity.dao.vista_dao import VistaDAO
from flaskr.Entity.dto.vista_dto import VistaDTO


class VistaService:
    def __init__(self):
        self.vista_dao = VistaDAO()

    def registrar_vista(self, descripcion: str, ruta: str, nombre: str):
        """Registra una nueva vista."""
        nueva_vista = VistaDTO(
            id_vista=0,
            descripcion=descripcion,
            fecha_creacion=datetime.now(),
            fecha_actualizacion=datetime.now(),
            fecha_eliminacion=None,
            ruta=ruta,
            nombre=nombre
        )

        return self.vista_dao.insertar_vista(nueva_vista)

    def obtener_todas_las_vistas(self):
        """Obtiene todas las vistas y las asigna al DTO."""
        vistas_bbdd = self.vista_dao.obtener_todas_las_vistas()
        lista_vistas = [
            VistaDTO(
                id_vista=vista[0],
                descripcion=vista[1],
                fecha_creacion=vista[2],
                fecha_actualizacion=vista[3],
                fecha_eliminacion=vista[4],
                ruta=vista[5],
                nombre=vista[6]
            ) for vista in vistas_bbdd
        ]
        return lista_vistas

    def actualizar_vista(self, id_vista, descripcion=None, ruta=None, nombre=None):
        """Actualiza una vista sin modificar la fecha de creación."""
        vista = self.vista_dao.obtener_por_id(id_vista)  # Asegura que obtenemos la vista

        if not vista:
            return False  # Si la vista no existe, retorna False

        # Convertimos la vista en un diccionario si aún no lo es
        vista_data = {
            "id_vista": id_vista,
            "descripcion": descripcion if descripcion else vista["descripcion"],
            "ruta": ruta if ruta else vista["ruta"],
            "nombre": nombre if nombre else vista["nombre"]
        }

        return self.vista_dao.actualizar_vista(vista_data)

    def borrar_vista(self, id_vista):
        """Realiza un borrado lógico de una vista marcando la fecha de eliminación."""
        if not isinstance(id_vista, int) or id_vista <= 0:
            raise ValueError("El id_vista debe ser un entero válido y mayor a 0.")

        resultado = self.vista_dao.borrar_vista_logicamente(id_vista)

        if resultado:
            return {"message": f"Vista con ID {id_vista} marcada como eliminada."}, 200
        else:
            return {"error": "No se pudo marcar la vista como eliminada."}, 400