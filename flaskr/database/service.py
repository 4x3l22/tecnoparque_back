from datetime import datetime
from .database import FirebaseConnection

class FirebaseService:
    def __init__(self):
        self.db = FirebaseConnection().get_db()
        if self.db is None:
            raise ValueError("No se pudo conectar a Firebase. Verifica FirebaseConnection.")

    def get_documents(self, collection: str):
        """Obtiene todos los datos de una colección en Firebase Realtime Database."""
        try:
            ref = self.db.child(collection)  # Referencia a la colección
            data = ref.get()  # Obtener los datos

            if data is None:
                return {"message": "No se encontraron documentos en la colección."}

            result = data.val() if hasattr(data, 'val') else data

            # 🔹 Convertir timestamp a fecha legible en cada documento
            for key, item in result.items():
                if 'timestamp' in item:
                    timestamp = item['timestamp']
                    item['fecha_hora'] = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

            return result
        except Exception as e:
            return {"error": f"Error al obtener documentos: {str(e)}"}
