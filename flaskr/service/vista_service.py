from flaskr.Entity.dao.vista_dao import VistaDAO


class VistaService:
    def __init__(self):
        self.dao = VistaDAO()

    # CREATE
    def insert_vista(self, vista_data):
        """
        Inserta una nueva vista en la base de datos.
        :param vista_data: Diccionario o DTO con los datos de la vista a insertar.
        """
        self.dao.insert_vista(vista_data)

    # READ - Obtener todos los registros
    def get_all_vistas(self):
        """
        Obtiene una lista de todas las vistas almacenadas en la base de datos.
        :return: Lista de vistas.
        """
        return self.dao.get_all_vistas()

    # READ - Obtener un registro por ID
    def get_vista_by_id(self, vista_id):
        """
        Obtiene una vista específica por su ID.
        :param vista_id: ID único de la vista.
        :return: Objeto de la vista o None si no existe.
        """
        return self.dao.get_vista_by_id(vista_id)

    # UPDATE
    def update_vista(self, vista_id, vista_data):
        """
        Actualiza una vista existente en la base de datos.
        :param vista_id: ID único de la vista a actualizar.
        :param vista_data: Diccionario o DTO con los datos a actualizar.
        """
        self.dao.update_vista(vista_id, vista_data)
