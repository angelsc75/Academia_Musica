from fastapi import FastAPI
from api.routes import router
from database import engine
from models import Base

app = FastAPI(title="Music School Management API")

# Create database tables
Base.metadata.create_all(bind=engine)

# Include the API router
app.include_router(router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
