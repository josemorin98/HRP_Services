# HRP Services

## Descripción

HRP Services es un sistema basado en una arquitectura de microservicios que permite la ingesta, validación y procesamiento de datos en formato CSV mediante una API desarrollada en FastAPI.

El sistema utiliza una configuración en formato JSON para interpretar los datos, validar su estructura y ejecutar procesos automatizados.

---

## Programas del sistema

El sistema está compuesto por los siguientes módulos:

* **Ingress API (FastAPI)**: Punto de entrada que recibe solicitudes y procesa los datos.
* **Tools**: Capa lógica que contiene funciones de validación, logging y conexión a la base de datos.
* **MongoDB**: Base de datos NoSQL donde se almacenan tareas, resultados y logs.
* **TaskScheduler**: Módulo encargado de la orquestación y ejecución de tareas.
* **Docker Compose**: Herramienta utilizada para desplegar los servicios en contenedores.

---

## Flujo del sistema

1. El usuario envía un archivo CSV junto con un JSON de configuración.
2. La API recibe la solicitud.
3. Se carga y procesa el archivo CSV.
4. Se interpretan las variables definidas en el JSON.
5. Se realizan validaciones (espaciales, temporales y de interés).
6. Se generan logs del proceso (Observables en terminal).
7. Los datos y tareas se almacenan en MongoDB.
8. El TaskScheduler ejecuta procesos de manera automatizada.

---

## Diagrama de arquitectura

![Arquitectura](/data/icon/Arquitectura.png)

---

## Arbol de carpetas


```
├── 📁 data
│   ├── 📁 icon
│   │   ├── 🖼️ Arquitectura.png
│   │   └── 📄 HRP_Paper-Icon.ico
│   └── 📄 U_Rates.csv
├── 📁 src
│   ├── 📁 IngressApi
│   │   ├── 🐳 Dockerfile
│   │   ├── 🐍 main.py
│   │   └── 📄 requirements.txt
│   ├── 📁 Stori
│   │   └── 🐍 stori_serv.py
│   ├── 📁 TaskScheduler
│   │   ├── 🐳 Dockerfile
│   │   ├── 🐍 main.py
│   │   └── 📄 requirements.txt
│   └── 📁 Tools
│       ├── 🐍 loggerClass.py
│       ├── 🐍 mongo_connection.py
│       ├── 🐍 utils.py
│       └── 🐍 utils_scheduler.py
├── 📁 test
│   ├── 📁 logIngressAPI
│   ├── ⚙️ input_config.json
│   └── 🐍 test_scheduler.py
├── ⚙️ .gitignore
├── 📝 README.md
├── ⚙️ docker-compose.yml
└── 📄 requirements.txt
```

---


## Instalación y despliegue

### Requisitos

* Docker
* Acceso a terminal

---

### Clonar el repositorio

```bash
git clone https://github.com/josemorin98/HRP_Services/tree/main
cd HRP_Services
```

---

### Ejecutar el proyecto

```bash
docker compose up --build
```

### Opcional (Detener el proyecto) 
``` bash
docker compose down
```

---

### Acceder a la API

Una vez levantado el sistema, abre en el navegador:
Ingresa link para poder visualizar que este funcionando correctamente 

Nota: te puede mandar al puerto 8000, solo cambialo al puerto 8001


```text
http://localhost:8001/docs
```

---

### Poder ejecutar la aplicación y la matriz STORI
Dentro del proyecto ingresa ala carpeta "test"

``` bash
cd test
```

Posteriormente ejecutar el test_scheduler.py (Poder ver el funcionamiento)

``` bash
python3 test_scheduler.py
```

---

## 👨‍💻 Autor

Encargado: Dr.José Carlos Morín García
Becario: Jesús Eduardo Leal Gámez
