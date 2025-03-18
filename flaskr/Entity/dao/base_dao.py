from datetime import datetime

import pytz

from flaskr.database.conx_mysql import MySQLConnection

def obtener_hora_actual():
    zona_horaria = pytz.timezone("America/Bogota")
    return datetime.now(zona_horaria).strftime('%Y-%m-%d %H:%M:%S')

class BaseRepository:
    def __init__(self):
        """Inicializa el repositorio base con una conexión a la base de datos."""
        self.connection = MySQLConnection().get_connection()

    def insert(self, table_name: str, columns: list, values: tuple):
        """
        Inserta un registro genérico en una tabla de la base de datos.

        :param table_name: Nombre de la tabla en la que se insertarán los datos
        :param columns: Lista de columnas en las que se insertarán los valores
        :param values: Tupla con los valores a insertar en las columnas correspondientes
        :return: el ID del registro insertado
        """
        # Construye la consulta de inserción dinámicamente
        columns_str = ", ".join(columns)
        placeholders = ", ".join(["%s"] * len(columns))
        query = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})"

        try:
            cursor = self.connection.cursor()
            cursor.execute(query, values)
            self.connection.commit()
            return cursor.lastrowid  # Retorna el ID del registro insertado
        except Exception as e:
            self.connection.rollback()
            raise Exception(f"Error al insertar en {table_name}: {e}")
        finally:
            cursor.close()

    def obtener_por_id(self, table_name: str, id_column: str, record_id):
        """
        Obtiene un registro por su ID de una tabla específica.

        :param table_name: Nombre de la tabla de donde se obtendrá el registro
        :param id_column: Nombre de la columna que representa el ID
        :param record_id: Valor del ID del registro a obtener
        :return: Un diccionario con el registro encontrado o None si no existe
        """
        cursor = self.connection.cursor(dictionary=True)  # Devuelve resultados como diccionarios
        query = f"SELECT * FROM {table_name} WHERE {id_column} = %s"
        try:
            cursor.execute(query, (record_id,))
            result = cursor.fetchone()
            return result
        except Exception as e:
            raise Exception(f"Error al obtener por ID en la tabla {table_name}: {e}")
        finally:
            cursor.close()


    def update(self, table_name: str, data: dict, where_field: str, where_value):
        """
        Actualiza un registro en la base de datos sin modificar campos no especificados.

        :param table_name: Nombre de la tabla a actualizar
        :param data: Diccionario con los campos y valores a actualizar
        :param where_field: Nombre del campo de condición (ej. 'id_vista')
        :param where_value: Valor del campo de condición
        :return: True si se actualizó correctamente, False en caso contrario
        """
        if not isinstance(data, dict):
            raise ValueError("El parámetro 'data' debe ser un diccionario con los datos de actualización.")

        data["fecha_actualizacion"] = obtener_hora_actual()

        set_clause = ", ".join([f"{key} = %s" for key in data.keys()])
        values = tuple(data.values()) + (where_value,)

        query = f"UPDATE {table_name} SET {set_clause} WHERE {where_field} = %s"

        try:
            cursor = self.connection.cursor()
            cursor.execute(query, values)
            self.connection.commit()
            return cursor.rowcount > 0  # Devuelve True si se actualizó alguna fila
        except Exception as e:
            self.connection.rollback()
            raise Exception(f"Error al actualizar {table_name}: {e}")
        finally:
            cursor.close()

    def delete(self, table_name: str, id_field: str, id_value):
        """
        Realiza un borrado lógico en una tabla colocando la fecha de eliminación.

        :param table_name: Nombre de la tabla donde se hará el borrado lógico.
        :param id_field: Nombre del campo que identifica el registro (ej. 'id_vista').
        :param id_value: Valor del identificador del registro a eliminar.
        :return: True si la operación fue exitosa, False en caso contrario.
        """
        fecha_eliminacion = obtener_hora_actual()  # Obtener la fecha actual
        query = f"""
        UPDATE {table_name} 
        SET fecha_eliminacion = %s 
        WHERE {id_field} = %s
        """

        try:
            cursor = self.connection.cursor()
            cursor.execute(query, (fecha_eliminacion, id_value))
            self.connection.commit()
            return cursor.rowcount > 0  # Devuelve True si se actualizó alguna fila
        except Exception as e:
            self.connection.rollback()
            raise Exception(f"Error al realizar el borrado lógico en {table_name}: {e}")
        finally:
            cursor.close()

    def get_all(self, table_name: str):
        """
        Obtiene todos los registros de una tabla.

        :param table_name: Nombre de la tabla de la cual obtener los datos.
        :return: Lista de registros como diccionarios.
        """
        query = f"SELECT * FROM tecnoparque.{table_name}"

        try:
            cursor = self.connection.cursor()  # Devuelve resultados como diccionarios
            cursor.execute(query)
            resultados = cursor.fetchall()
            return resultados
        except Exception as e:
            raise Exception(f"Error al obtener datos de {table_name}: {e}")
        finally:
            cursor.close()