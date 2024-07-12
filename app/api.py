from fastapi import APIRouter
from api import students, teachers, instruments, auth

api_router = APIRouter()
api_router.include_router(auth.router, tags=["auth"])
api_router.include_router(students.router, prefix="/students", tags=["students"])
api_router.include_router(teachers.router, prefix="/teachers", tags=["teachers"])
api_router.include_router(instruments.router, prefix="/instruments", tags=["instruments"])
