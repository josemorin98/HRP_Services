FROM python:3.11-slim

# Crear directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar requirements desde la raíz del proyecto
COPY . /app/

# Instalar dependencias
RUN pip install -r requirements.txt

# # Copiar todo el código fuente necesario
# COPY ../Tools/   /app/src/Tools

# # Ir directo a la carpeta de IngressApi
# WORKDIR /app/src/IngressApi


# Exponer el puerto 8000
EXPOSE 8000

# Ejecutar main.py por defecto
# CMD [ ""]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

