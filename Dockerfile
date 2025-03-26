# Usa una imagen base con Python (versión estable más reciente)
FROM python:3.13-slim

# Establece el autor del archivo
LABEL authors="sena"

# Configura el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los requisitos (requirements.txt) al contenedor
COPY requirements.txt .

# Instala las dependencias necesarias
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copia todos los archivos del proyecto al contenedor
COPY . .

# Expone el puerto que utilizará la aplicación (por ejemplo, 5000 para Flask)
EXPOSE 5000

# Configura variables de entorno para Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=production
# Cambia a 'development' si es necesario

# Define el comando de inicio predeterminado
CMD ["flask", "run"]
