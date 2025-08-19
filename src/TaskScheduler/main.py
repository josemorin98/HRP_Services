# Sin contenedores
from src.Tools.loggerClass import FileLogger
from src.Tools.utils import Utils
from src.Tools.mongo_connection import MongoConnection
from src.Tools.utils_scheduler import Utils_scheduler

# Con contenedores
# from Tools.loggerClass import FileLogger
# from Tools.utils import Utils
# from Tools.mongo_connection import MongoConnection

# Importar FastAPI y otros módulos necesarios
from fastapi import FastAPI, HTTPException

from fastapi.responses import JSONResponse
from fastapi.responses import FileResponse
from fastapi import Request
from fastapi import UploadFile, File
import pandas as pd
import os
import time
import datetime
import hashlib
import uuid
import json


app = FastAPI()
logger = FileLogger(log_dir='./test/logTasksScheduler', log_name='taskScheduler')
mongo_tasks = MongoConnection(host="127.0.0.1", db_name="tasks")
mongo_matrix = MongoConnection(host="127.0.0.1", db_name="matrix")

@app.get("/")
def root():
    return JSONResponse(content={"message": "TaskScheduler API Running"})


@app.post("/process_config")
async def process_config(request: Request):
    try:
        # Leer el id_task del request
        data = await request.json()
        id_task = data.get("taskid")
        _id = data.get("_id")
        if not id_task:
            raise HTTPException(status_code=400, detail="Falta el parámetro id_task en el body.")

        # Buscar el documento en la colección tasks
        if mongo_tasks.conect() == False:
            raise HTTPException(status_code=500, detail="No se pudo conectar a la base de datos.")
        logger.error(f"Buscando task con id {id_task} y _id {_id}")
        status, task_doc = mongo_tasks.get_values('tasks', {'taskid': id_task})
        print("------",status, type(task_doc))
        mongo_tasks.close()

        if status != 200:
            raise HTTPException(status_code=404, detail=f"No se encontró la task con id {id_task}, {_id}")

        config = task_doc.get("observatory", None)
        if config == None:
            raise HTTPException(status_code=400, detail="No se encontró el campo 'config' en la task.")

        print(f"Configuración de la tarea: {config}")
        # Leer el CSV
        csv_path = config.get("csv_path", None)
        print(f"Ruta del CSV: {csv_path}")
        if csv_path is None:
            raise HTTPException(status_code=400, detail="csv_path no especificado en la configuración.")
        csv_full_path = os.path.join(os.path.dirname(__file__), csv_path)
        if not os.path.exists(csv_full_path):
            raise HTTPException(status_code=400, detail=f"No se encontró el archivo CSV en {csv_full_path}")
        df = pd.read_csv(csv_full_path)

        # Procesar Levels
        levels = config.get("Levels", [])
        print(levels)
        combos = Utils_scheduler.get_level_combinations(df, levels)

        return {"id_task": id_task, "combinations_by_level": combos}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesando el archivo: {e}")

@app.get("/tasks")
def get_tasks():
    """
    Endpoint que retorna todos los valores de la colección 'tasks' en MongoDB.
    """
    if not mongo_tasks.conect():
        return {"error": "No se pudo conectar a la base de datos"}
    tasks = mongo_tasks.get_values("tasks")
    mongo_tasks.close()
    # Convertir ObjectId a string para JSON serializable
    for t in tasks:
        t["taskid"] = str(t["taskid"])
    return {"tasks": tasks}
