from datetime import datetime

import pytz

from flaskr.Entity.dto.vista_dto import VistaDTO
from flaskr.database.conx_mysql import MySQLConnection

def obtener_hora_actual():
    zona_horaria = pytz.timezone("America/Bogota")
    return datetime.now(zona_horaria).strftime('%Y-%m-%d %H:%M:%S')

class VistaDAO:
    def __init__(self):
        self.connection = MySQLConnection().get_connection()

    def insertar_vista(self, vista: VistaDTO):
        """Inserta una nueva vista en la base de datos."""
        query = """
        INSERT INTO vistas (descripcion, fecha_creacion, fecha_actualizacion, fecha_eliminacion, ruta, nombre)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (vista.descripcion, vista.fecha_creacion, vista.fecha_actualizacion,
                  vista.fecha_eliminacion, vista.ruta, vista.nombre)

        try:
            cursor = self.connection.cursor()
            cursor.execute(query, values)
            self.connection.commit()
            return cursor.lastrowid  # Retorna el ID de la vista insertada
        except Exception as e:
            self.connection.rollback()
            raise Exception(f"Error al insertar vista: {e}")
        finally:
            cursor.close()

    def obtener_todas_las_vistas(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM tecnoparque.vistas")
        vistas = cursor.fetchall()
        cursor.close()
        return vistas

    def obtener_por_id(self, id_vista):
        """Obtiene una vista por su ID."""
        cursor = self.connection.cursor(dictionary=True)  # Devuelve resultados como diccionarios
        query = "SELECT * FROM vistas WHERE id_vista = %s"
        cursor.execute(query, (id_vista,))
        vista = cursor.fetchone()
        cursor.close()
        return vista  # Devuelve None si no encuentra la vista

    def actualizar_vista(self, vista):
        """Actualiza una vista en la base de datos sin modificar fecha_creacion."""
        cursor = self.connection.cursor()
        fecha_actual = obtener_hora_actual()  # Obtener la fecha actual

        query = """
        UPDATE vistas 
        SET descripcion = %s, ruta = %s, nombre = %s, fecha_actualizacion = %s
        WHERE id_vista = %s
        """

        # Asegurar que "vista" es un diccionario
        if not isinstance(vista, dict):
            raise ValueError("El parámetro 'vista' debe ser un diccionario con los datos de actualización.")

        # CORRECTO: fecha_actual antes de id_vista
        cursor.execute(query, (vista["descripcion"], vista["ruta"], vista["nombre"], fecha_actual, vista["id_vista"]))

        self.connection.commit()
        cursor.close()

        return True

    def borrar_vista_logicamente(self, id_vista):
        """Marca una vista como eliminada colocando la fecha de eliminación."""
        cursor = self.connection.cursor()
        fecha_eliminacion = obtener_hora_actual()  # Obtener la fecha actual en Bogotá

        query = """
        UPDATE vistas 
        SET fecha_eliminacion = %s
        WHERE id_vista = %s
        """

        cursor.execute(query, (fecha_eliminacion, id_vista))
        self.connection.commit()
        cursor.close()

        return True
