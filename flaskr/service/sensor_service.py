from datetime import datetime

from flaskr.Entity.dao.sensor_dao import SensorDAO
from flaskr.Entity.dto.sensor_dto import SensorDTO


class FirebaseService:
    def __init__(self):
        self.dao = SensorDAO()

    def get_sensor_data(self, collection):
        data = self.dao.get_all_documents(collection)  # data es una lista
        response = []

        for item in data:  # Iteramos directamente sobre la lista
            if 'timestamp' in item:
                item['fecha_hora'] = datetime.fromtimestamp(item['timestamp']).strftime('%Y-%m-%d %I:%M:%S %p')

            dto = SensorDTO(item['humedad'], item['temperatura'], item.get('fecha_hora', ''))
            response.append(dto.__dict__)

        return response
    
    def get_end_rows(self, collection):
        data = self.dao.get_end_rows(collection)
        response = []

        for item in data:
            if 'timestamp' in item:
                item['fecha_hora'] = datetime.fromtimestamp(item['timestamp']).strftime('%Y-%m-%d %I:%M:%S %p')

            dto = SensorDTO(item['humedad'], item['temperatura'], item.get('fecha_hora', ''))
            response.append(dto.__dict__)
        return response
    
    def get_sensor_data_by_date(self, collection, start_date, end_date):
            data = self.dao.get_documents_by_date(collection, start_date, end_date)
            response = []

            for item in data:
                if 'timestamp' in item:
                    item['fecha_hora'] = datetime.fromtimestamp(item['timestamp']).strftime('%Y-%m-%d %I:%M:%S %p')

                dto = SensorDTO(item['humedad'], item['temperatura'], item.get('fecha_hora', ''))
                response.append(dto.__dict__)

            return response