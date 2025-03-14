import firebase_admin
from firebase_admin import credentials, db
import os

class FirebaseConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FirebaseConnection, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Inicializa la conexión con Firebase Realtime Database."""
        # Obtener rutas de variables de entorno
        service_account_path = os.getenv("SERVICE_ACCOUNT_PATH")
        database_url = os.getenv("DATABASE_URL")

        # Si la ruta no es absoluta, convertirla a absoluta
        if service_account_path and not os.path.isabs(service_account_path):
            base_dir = os.path.dirname(os.path.abspath(__file__))
            service_account_path = os.path.join(base_dir, service_account_path)

        # Verificar que el archivo existe
        if not service_account_path or not os.path.exists(service_account_path):
            raise FileNotFoundError(f"⚠️ ERROR: No se encontró el archivo de credenciales en '{service_account_path}'")

        # Verificar que la URL de la base de datos está definida
        if not database_url:
            raise ValueError("⚠️ ERROR: La variable de entorno 'DATABASE_URL' no está definida")

        # Inicializar Firebase solo si no está inicializado
        if not firebase_admin._apps:
            self.cred = credentials.Certificate(service_account_path)
            self.app = firebase_admin.initialize_app(self.cred, {'databaseURL': database_url})
        self.db = db.reference()

    def get_db(self):
        """Retorna la instancia de la base de datos Realtime Database."""
        return self.db
