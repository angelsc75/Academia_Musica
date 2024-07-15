from fastapi import FastAPI
from routes import router
from db import engine
from models import Base
from logging_config import setup_logger

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