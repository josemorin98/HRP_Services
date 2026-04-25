import requests
import json
from pathlib import Path

# URL del servicio al que quieres hacer la petición
url = "http://localhost:8001/generateObservatory"

json_path = Path(__file__).with_name("input_config.json")

# Validar que el JSON local sea correcto antes de enviarlo
with open(json_path, "r", encoding="utf-8") as f:
    payload = json.load(f)

print(type(payload))
print(payload)
response = requests.post(url, json=payload, timeout=60)

# Mostrar el resultado
print("Status code:", response.status_code)
print("Response:", response.text)

try:
    print("Response JSON:", json.dumps(response.json(), indent=2, ensure_ascii=False))
except ValueError:
    print("La respuesta no es JSON válido.")
