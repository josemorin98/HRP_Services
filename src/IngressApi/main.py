# Sin contenedores
# from src.Tools.loggerClass import FileLogger
# from src.Tools.utils import Utils
# from src.Tools.mongo_connection import MongoConnection


# Con contenedores
from Tools.loggerClass import FileLogger
from Tools.utils import Utils
from Tools.mongo_connection import MongoConnection

# Importar FastAPI y otros módulos necesarios
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.responses import FileResponse
from fastapi import Request
import pandas as pd
import os
import time
import datetime
import hashlib
import uuid

app = FastAPI()
logger = FileLogger(log_dir='./test/logIngressAPI', log_name='ingressAPI')
mongo = MongoConnection(db_name="tasks")
    

@app.get("/")
def read_root():
    return {"message": "¡Hola, mundo soy tu orquestador morin"}

# @app.get("/favicon.ico")
# async def favicon():
#     return FileResponse("\home\jmorin\jcmg_HRP_Service\data\icon\HRP_Paper-Icon.ico")

# Endpoint para saber el directorio actual del servidor
@app.get("/get_cwd")
async def get_cwd():
    cwd = os.getcwd()
    return {"cwd": cwd}


@app.post("/generateObservatory")
async def generateObservatory(request: Request):
    start_time = time.time()
    try:
        config = await request.json()
        print(f"JSON recibido: {config}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error leyendo el JSON recibido:\n {e}")
    print(f"Configuración recibida")
    observatory = config.get('observatory')
    if not observatory:
        raise HTTPException(status_code=400, detail="No se encontró 'observatory' en el JSON")
    csv_path = observatory.get('csv_path')
    if not csv_path:
        raise HTTPException(status_code=400, detail="No se encontró 'csv_path' en observatory")

    tiempo_lectura = time.time() - start_time
    print(f"Tiempo de lectura de confiugracion: {tiempo_lectura} segundos")

    try:
        # Si la ruta no es absoluta, la buscamos relativa al directorio del servidor
        start_time_csv = time.time()
        if not os.path.isabs(csv_path):
            csv_path = os.path.abspath(csv_path)
        # Realiza la lectura del CSV
        # print(os.getcwd())
        df = pd.read_csv(csv_path)

        tiempo_lectura_csv = time.time() - start_time_csv
        print(f"Tiempo de lectura del CSV: {tiempo_lectura_csv} segundos")

        start_time_verification = time.time()
        # -----------------------------------------------------------------------------------
        # Verificación específica para variables espaciales
        spatial_vars = config.get('spatialVariables', {})
        spatial_results = {}
        for spatial_key, spatial_col in spatial_vars.items():
            spatial_results[spatial_key] = Utils.verificar_variable_espacial(df, spatial_key, spatial_col, logger)
        print(f"Resultados de verificación espacial: {spatial_results}")
        print(Utils.verificar_jerarquia_espacial(spatial_results, logger))
        
        
        # -----------------------------------------------------------------------------------
        # Verificación de variable temporal
        temporal_vars = config.get('temporalVariables', {})
        temporal_ok = Utils.verificar_variable_temporal(df, temporal_vars, logger)
        print(f"Resultado de verificación temporal: {temporal_ok}")
        
        
        # -----------------------------------------------------------------------------------
        # Verificación de variable de interés
        interest_vars = config.get('interestVariables', {})
        interest_ok = Utils.verificar_variable_interes(df, interest_vars, logger)
        print(f"Resultado de verificación de interés: {interest_ok}")

        # -----------------------------------------------------------------------------------
        # Verificación de variable de observación
        observation_vars = config.get('observationVariables', {})
        observation_ok = Utils.verificar_variable_interes(df, observation_vars, logger)
        print(f"Resultado de verificación de observación: {observation_ok}")

        tiempo_verificacion = time.time() - start_time_verification
        print(f"Tiempo de verificación: {tiempo_verificacion} segundos")

        start_time_insert = time.time()
        # Generar un taskid único
        taskid = generar_taskid()
        print(f"TaskID generado: {taskid}")

        # Conectar a la base de datos MongoDB
        if mongo.conect()==True:
            db = mongo.get_db()
            # Aquí puedes realizar operaciones con la base de datos,
            # taskid
            print(type(config))
            insert_json = {"taskid": taskid, 
                           "timestamp": datetime.datetime.utcnow(), 
                           "observatory": config}
            insertStatus = mongo.insert_value("tasks", insert_json)
            print(f"Insert Status: {insertStatus}")
            mongo.close()
        else:
            logger.error("No se pudo conectar a la base de datos MongoDB")
        tiempo_insert = time.time() - start_time_insert
        print(f"Tiempo de inserción en MongoDB: {tiempo_insert} segundos")
        # si todo sale correcto dentro de la verificación, pasa a enviarlo al orquestador
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error leyendo el CSV: {e}")

    logger.info(f"READ_CONFIG_TIME\t{tiempo_lectura}\tREAD_CSV_TIME\t{tiempo_lectura_csv}\tVERIFICATION_TIME\t{tiempo_verificacion}\tINSERTION_TIME\t{tiempo_insert}")
    responseContent = {"csv_preview": "OKOK",
                       "id_task": taskid}
    return JSONResponse(content=responseContent, status_code=200)


@app.get("/tasks")
def get_tasks():
    """
    Endpoint que retorna todos los valores de la colección 'tasks' en MongoDB.
    """
    if not mongo.conect():
        return {"error": "No se pudo conectar a la base de datos"}
    tasks = mongo.get_values("tasks")
    mongo.close()
    # Convertir ObjectId a string para JSON serializable
    for t in tasks:
        t["taskid"] = str(t["taskid"])
    return {"tasks": tasks}


def generar_taskid():
    """
    Genera un taskid único usando uuid4 y lo hashea con SHA256.
    """
    unique_id = str(uuid.uuid4())
    hash_object = hashlib.sha256(unique_id.encode())
    return hash_object.hexdigest()




