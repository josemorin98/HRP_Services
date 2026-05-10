FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt /app/
COPY src/ /app/src/

RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app/src/TaskScheduler
#Modificacion para que docker detecte donde este el main.py a ejecutar
ENV PYTHONPATH=/app 

EXPOSE 8100

#Aca igual se modifico el comando para que ejecute el main.py correcto
CMD ["uvicorn", "src.TaskScheduler.main:app", "--host", "0.0.0.0", "--port", "8100"]
