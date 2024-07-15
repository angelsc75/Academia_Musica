from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from app.core.config import settings
from app.routes import students, teachers
from app.db import engine
from app import models
from app.crud import auth

app = FastAPI(title="API Escuela de música")

# Create database tables
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)
models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router, tags=["authentication"])
app.include_router(students.router, prefix="/students", tags=["students"])
app.include_router(teachers.router, prefix="/teachers", tags=["teachers"])
app.include_router(instruments.router, prefix="/instruments", tags=["instruments"])
app.include_router(inscriptions.router, prefix="/inscriptions", tags=["inscriptions"])
app.include_router(levels.router, prefix="/levels", tags=["levels"])
app.include_router(packs.router, prefix="/packs", tags=["packs"])
app.include_router(teacher_instruments.router, prefix="/teacher-instruments", tags=["teacher_instruments"])
app.include_router(pack_instruments.router, prefix="/pack-instruments", tags=["pack_instruments"])
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
