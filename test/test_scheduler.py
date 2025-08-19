import requests
import json
import tempfile
import os

# URL del servicio al que quieres hacer la petición
url = "http://localhost:8000/process_config"

jsonPath = "./input_config.json"

# Leer el archivo JSON y guardarlo temporalmente como archivo para enviar
with open(jsonPath, "r", encoding="utf-8") as f:
    payload = json.load(f)

with tempfile.NamedTemporaryFile(delete=False, suffix='.json', mode='w', encoding='utf-8') as tmp:
    json.dump(payload, tmp)
    tmp_path = tmp.name

with open(tmp_path, "rb") as f:
    files = {"file": (os.path.basename(jsonPath), f, "application/json")}
    response = requests.post(url, files=files)

# Eliminar el archivo temporal
os.remove(tmp_path)

# Mostrar el resultado
print("Status code:", response.status_code)
print("Response:", response.text)
