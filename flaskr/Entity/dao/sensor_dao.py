from datetime import datetime, UTC
from flaskr.database.database import FirebaseConnection


class SensorDAO:
    def __init__(self):
        self.db = FirebaseConnection().get_db()

    def get_all_documents(self, collection):
        try:
            # Referencia a la colección en Firebase
            ref = self.db.child(collection)
            data = ref.get()  # Obtén los datos

            # Si no hay datos, devuelve una lista vacía
            if not data:
                return []

            # Si los datos ya son una lista, devuélvelos directamente
            if isinstance(data, list):
                return data

            # Si los datos son un diccionario, conviértelos en lista
            return [{**value, "id": key} for key, value in data.items()]
        except Exception as e:
            print(f"Error al obtener documentos: {e}")
            return []

    def get_end_rows(self, collection):
        ref = self.db.child(collection)
        data = ref.get()

        if not data:
            return []

        # 🔹 Convertir los documentos de diccionario a lista
        documents = [{**value, "id": key} for key, value in data.items()]

        # 🔹 Tomar solo los últimos 5 documentos insertados
        return documents[-5:] if len(documents) > 5 else documents

    def get_documents_by_date(self, collection, start_date, end_date):
        ref = self.db.child(collection)
        data = ref.get()

        if not isinstance(data, dict):  # Asegúrate de que los datos sean un diccionario
            return []

        try:
            # Convertir fechas a timestamps (en UTC)
            start_timestamp = datetime.strptime(start_date, "%Y-%m-%d").replace(tzinfo=UTC).timestamp()
            end_timestamp = datetime.strptime(end_date, "%Y-%m-%d").replace(tzinfo=UTC).timestamp()
        except ValueError:
            raise ValueError("Las fechas deben estar en el formato 'YYYY-MM-DD'")

        # Convertir los documentos a una lista con validación de "timestamp"
        documents = [
            {**value, "id": key} for key, value in data.items()
            if isinstance(value.get("timestamp", None), (int, float))
        ]

        # Filtrar documentos por rango de fechas
        filtered_documents = [
            doc for doc in documents
            if start_timestamp <= doc["timestamp"] <= end_timestamp
        ]

        return filtered_documents