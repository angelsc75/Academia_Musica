from fastapi import FastAPI
from routes import router
from db import engine
from models import Base
from logging_config import setup_logger

'''
Este código configura una aplicación de FastAPI con soporte de logging y gestión de base de datos. 
Cuando se ejecuta, inicia un servidor Uvicorn que sirve la aplicación en http://127.0.0.1:8000.
'''
app = FastAPI(title="API Escuela de música")

# Configurar el logger
logger = setup_logger()

# Create database tables
Base.metadata.create_all(bind=engine)

# Include the API router
app.include_router(router, prefix="")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
