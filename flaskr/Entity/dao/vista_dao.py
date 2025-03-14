from flaskr.database.conx_mysql import MySQLConnection

class VistaDAO:

    def __init__(self):
        self.conn = MySQLConnection().get_connection()
        self.cursor = self.conn.cursor()

    # CREATE
    def insert_vista(self, vista_data):
        """
        Inserta un nuevo registro en la tabla vistas.
        :param vista_data: Tupla con los datos (nombre, descripcion, ruta, fecha_creacion).
        """
        query = "INSERT INTO vistas (nombre, descripcion, ruta, fecha_creacion) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(query, vista_data)
        self.conn.commit()

    # READ - Obtener todos los registros
    def get_all_vistas(self):
        """
        Obtiene todos los registros de la tabla vistas.
        :return: Lista de tuplas, donde cada tupla representa un registro en la tabla vistas.
        """
        query = "SELECT * FROM vistas"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    # READ - Obtener un registro por ID
    def get_vista_by_id(self, vista_id):
        """
        Obtiene un registro específico de la tabla vistas por su ID.
        :param vista_id: ID del registro a obtener.
        :return: Una tupla con el registro si existe, None si no.
        """
        query = "SELECT * FROM vistas WHERE id = %s"
        self.cursor.execute(query, (vista_id,))
        return self.cursor.fetchone()

    # UPDATE
    def update_vista(self, vista_id, vista_data):
        """
        Actualiza los datos de una vista por su ID.
        :param vista_id: ID único de la vista a actualizar.
        :param vista_data: Diccionario con los campos a actualizar y sus nuevos valores.
        """
        query = """
            UPDATE vistas 
            SET nombre = %s, descripcion = %s, ruta = %s, fecha_creacion = %s 
            WHERE id = %s
        """
        data = (
            vista_data.get('nombre'),
            vista_data.get('descripcion'),
            vista_data.get('ruta'),
            vista_data.get('fecha_creacion'),
            vista_id
        )
        self.cursor.execute(query, data)
        self.conn.commit()
