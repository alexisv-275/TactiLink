# Imagen base para Python (usa una versión slim para ser más ligera)
# SE CAMBIA A 3.11 POR SER UNA VERSIÓN ESTABLE Y OFICIAL EN DOCKER HUB
FROM python:3.11-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar el archivo de dependencias e instalarlas (para aprovechar el cache de Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY . .

# Comando para correr la aplicación Flask
CMD ["python", "app.py"] 

# Exponer el puerto interno de Flask
EXPOSE 5000

