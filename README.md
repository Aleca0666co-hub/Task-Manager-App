
# TodoApp (FastAPI + SQLAlchemy)

 English 🇬🇧

*Sample application to manage tasks using FastAPI, SQLAlchemy, and Pydantic.  
It includes REST endpoints, validations, and a modular structure designed to scale.*

## 🚀 Features
- CRUD endpoints for tasks (POST /tasks, GET /tasks).
- ORM models with SQLAlchemy and polymorphic inheritance (BaseTask, Task).
- Validations with Pydantic (TaskCreate, TaskRead).
- Logging configured for debugging.
- Modular architecture (api, models, schemas, crud, database, utils).

## 📂 Project Structure
```

todo_app/
├── app/
│   ├── main.py             
│   ├── settings.py           
│   ├── models/
│   │   ├── base.py         
│   │   └── task.py         
│   ├── schemas/
│   │   └── task.py         
│   ├── crud/
│   │   └── task.py         
│   ├── api/
│   │   └── task.py         
│   ├── database.py         
│   └── utils/
│        ├──logging.py
│        └──exceptions.py
├──logs/
│    └──app.log
├──poetry.lock
├──pyproject.toml
├── alembic/                
├── requirements.txt
└── README.md

```

## ⚙️ Installation  
Requirements: Python 3.12.11

`bash
python -m venv .venv
source .venv/bin/activate   # Linux/Mac

On Windows
.venv\Scripts\activate
pip install -r requirements.txt
`

## ▶️ Run the application
`bash
uvicorn app.main:app --reload
`

Automatic documentation:  
- http://localhost:8000/docs
- http://localhost:8000/redoc


## 🧪 Testing
Run tests with:
`bash
pytest
`

## 📜 License  
This project is licensed under the MIT License – see the LICENSE file for details.

---

Español 🇪🇸

*Aplicación de ejemplo para gestionar tareas usando FastAPI, SQLAlchemy y Pydantic.  
Incluye endpoints REST, validaciones y estructura modular para escalar.*

## 🚀 Características
- Endpoints CRUD para tareas (POST /tasks, GET /tasks).
- Modelos ORM con SQLAlchemy y herencia polimórfica (BaseTask, Task).
- Validaciones con Pydantic (TaskCreate, TaskRead).
- Logging configurado para depuración.
- Arquitectura modular (api, models, schemas, crud, database, utils).

## 📂 Estructura del proyecto
```

todo_app/
├── app/
│   ├── main.py             
│   ├── settings.py           
│   ├── models/
│   │   ├── base.py         
│   │   └── task.py         
│   ├── schemas/
│   │   └── task.py         
│   ├── crud/
│   │   └── task.py         
│   ├── api/
│   │   └── task.py         
│   ├── database.py         
│   └── utils/
│        ├──logging.py
│        └──exceptions.py
├──logs/
│    └──app.log
├──poetry.lock
├──pyproject.toml
├── alembic/                
├── requirements.txt
└── README.md

```
## ⚙️ Instalación  
Requisitos: Python 3.12.11

`bash
python -m venv .venv
source .venv/bin/activate   # Linux/Mac

En Windows
.venv\Scripts\activate
pip install -r requirements.txt
`

## ▶️ Ejecución
`bash
uvicorn app.main:app --reload
`

Documentación automática: 
- http://localhost:8000/docs
- http://localhost:8000/redoc

## 🧪 Testing  
Ejecuta pruebas con:
`bash
pytest
`

## 📜 Licencia  
Este proyecto está bajo la licencia MIT – consulta el archivo LICENSE para más detalles.


