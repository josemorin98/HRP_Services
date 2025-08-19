FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt /app/
COPY src/ /app/src/

RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app/src/TaskSheduler

EXPOSE 8100

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8100"]
