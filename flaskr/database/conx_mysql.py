import mysql.connector
from mysql.connector import Error
from flaskr.database.Cnx_mysql.config import Config


class MySQLConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MySQLConnection, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Inicializa la conexión con MySQL."""
        try:
            self.connection = mysql.connector.connect(
                host=Config.MYSQL_HOST,
                user=Config.MYSQL_USER,
                password=Config.MYSQL_PASSWORD,
                database=Config.MYSQL_DATABASE
            )
            if self.connection.is_connected():
                print("✅ Conexión a MySQL establecida correctamente")
        except Error as e:
            raise ConnectionError(f"⚠️ ERROR: No se pudo conectar a MySQL: {e}")

    def get_connection(self):
        """Retorna la instancia de la conexión MySQL."""
        return self.connection
