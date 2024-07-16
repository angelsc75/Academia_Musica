from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from core.config import settings
from db import engine
from models import Base
from crud.auth import router as auth_router
from crud.students_crud import router as students_router
from crud.teacher_crud import router as teachers_router
from crud.instruments_crud import router as instruments_router
from crud.inscriptions_crud import router as inscriptions_router
from crud.levels_crud import router as levels_router
from crud.packs_crud import router as packs_router
from crud.teacher_instruments_crud import router as teacher_instruments_router
from crud.pack_instruments_crud import router as pack_instruments_router

app = FastAPI(title="API Escuela de música")

# Create database tables
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)
Base.metadata.create_all(bind=engine)

app.include_router(auth_router, tags=["authentication"])
app.include_router(students_router, prefix="/students", tags=["students"])
app.include_router(teachers_router, prefix="/teachers", tags=["teachers"])
app.include_router(instruments_router, prefix="/instruments", tags=["instruments"])
app.include_router(inscriptions_router, prefix="/inscriptions", tags=["inscriptions"])
app.include_router(levels_router, prefix="/levels", tags=["levels"])
app.include_router(packs_router, prefix="/packs", tags=["packs"])
app.include_router(teacher_instruments_router, prefix="/teacher-instruments", tags=["teacher_instruments"])
app.include_router(pack_instruments_router, prefix="/pack-instruments", tags=["pack_instruments"])
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
