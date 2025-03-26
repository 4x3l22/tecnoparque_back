from datetime import datetime, timezone

import pytz

from flaskr.Entity.dao.sensor_dao import SensorDAO
from flaskr.Entity.dto.sensor_dto import SensorDTO


class FirebaseService:
    def __init__(self):
        self.dao = SensorDAO()

    def get_sensor_data(self, collection):
        try:
            # Obtener los datos de la colección
            data = self.dao.get_all_documents(collection)  # data es una lista
            response = []

            for item in data:  # Iteramos directamente sobre la lista
                # Convertir timestamp a fecha_hora si está disponible
                fecha_hora = ''
                if 'timestamp' in item:
                    try:
                        fecha_hora = datetime.fromtimestamp(item['timestamp']).strftime('%Y-%m-%d %I:%M:%S %p')
                    except (ValueError, TypeError):
                        fecha_hora = 'Fecha inválida'

                # Crear el DTO asegurando que todos los campos están presentes
                humedad = item.get('humedad', None)
                temperatura = item.get('temperatura', None)

                # Asegúrate de que SensorDTO acepte valores opcionales o reemplázalos con valores predeterminados
                dto = SensorDTO(humedad, temperatura, fecha_hora)
                response.append(dto.__dict__)  # Convierte a diccionario

            return response

        except Exception as e:
            print(f"Error al obtener datos del sensor: {e}")
            return []

    def get_end_rows(self, collection):
        data = self.dao.get_end_rows(collection)
        response = []

        # Definir la zona horaria de Bogotá
        bogota_tz = pytz.timezone("America/Bogota")

        for item in data:
            if 'timestamp' in item:
                try:
                    # Asegúrate de que el timestamp sea un número
                    timestamp = float(item['timestamp'])

                    # Convertir el timestamp a la zona horaria de Bogotá
                    item['fecha_hora'] = datetime.fromtimestamp(timestamp, tz=pytz.utc).astimezone(bogota_tz).strftime(
                        '%Y-%m-%d %I:%M:%S %p')
                except (ValueError, TypeError):
                    # Manejar casos en que el timestamp no sea válido
                    item['fecha_hora'] = 'Fecha inválida'

            # Crear el DTO
            dto = SensorDTO(item['humedad'], item['temperatura'], item.get('fecha_hora', ''))
            response.append(dto.__dict__)

        return response

    def get_sensor_data_by_date(self, collection, start_date, end_date):
        data = self.dao.get_documents_by_date(collection, start_date, end_date)
        response = []

        # Definir la zona horaria de Bogotá
        bogota_tz = pytz.timezone("America/Bogota")

        for item in data:
            if 'timestamp' in item:
                try:
                    # Asegúrate de que el timestamp sea un número
                    timestamp = float(item['timestamp'])

                    # Convertir el timestamp a la zona horaria de Bogotá
                    item['fecha_hora'] = datetime.fromtimestamp(timestamp, tz=pytz.utc).astimezone(bogota_tz).strftime(
                        '%Y-%m-%d %I:%M:%S %p')
                except (ValueError, TypeError):
                    # Manejar casos en que el timestamp no sea válido
                    item['fecha_hora'] = 'Fecha inválida'

            # Crear el DTO
            dto = SensorDTO(item['humedad'], item['temperatura'], item.get('fecha_hora', ''))
            response.append(dto.__dict__)

        return response