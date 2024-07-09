from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db import SessionLocal
from app.crud import teacher_crud as crud
from . import schemas

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/teachers/{teacher_id}", response_model=schemas.Teacher)
def read_teacher(teacher_id: int, db: Session = Depends(get_db)):
    db_teacher = crud.get_teacher(db, teacher_id)
    if db_teacher is None:
        raise HTTPException(status_code=404, detail="Profesor no encontrado")
    return db_teacher

@app.get("/teachers/", response_model=List[schemas.Teacher])
def read_teachers(db: Session = Depends(get_db)):
    teachers = crud.get_teachers(db)
    if teachers is None:
        raise HTTPException(status_code=404, detail="Ningún profesor registrado")
    return teachers

@app.post("/teachers/", response_model=schemas.Teacher)
def create_teacher(teacher: schemas.CreateTeacher, db: Session = Depends(get_db)):
    teacher = crud.create_teacher(db, teacher=teacher)
    if teacher is None:
        raise HTTPException(status_code=404, detail="Ya existe el profesor")
    return teacher
