from datetime import datetime
from flaskr.database.database import FirebaseConnection


class SensorDAO:
    def __init__(self):
        self.db = FirebaseConnection().get_db()

    def get_all_documents(self, collection):
        ref = self.db.child(collection)
        data = ref.get()

        if not data:
            return []

        if isinstance(data, list):  # 🔹 Si ya es una lista, ordenar directamente
            return sorted(data, key=lambda x: x.get("timestamp", 0), reverse=True)

        # 🔹 Si es un diccionario, convertirlo en lista antes de ordenar
        documents = [{**value, "id": key} for key, value in data.items()]
        sorted_documents = sorted(documents, key=lambda x: x.get("timestamp", 0), reverse=True)

        return sorted_documents
    
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

        if not data:
            return []

        # Convertir fechas a timestamps
        start_timestamp = datetime.strptime(start_date, "%Y-%m-%d").timestamp()
        end_timestamp = datetime.strptime(end_date, "%Y-%m-%d").timestamp()

        # Convertir los documentos de diccionario a lista
        documents = [{**value, "id": key} for key, value in data.items()]

        # Filtrar los documentos por el rango de fechas
        filtered_documents = [
            doc for doc in documents
            if start_timestamp <= doc.get("timestamp", 0) <= end_timestamp
        ]

        return filtered_documents