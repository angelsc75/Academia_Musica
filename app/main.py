from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from decimal import Decimal

from app.db import SessionLocal
from app.crud import teacher_crud, instruments_crud
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
    db_teacher = teacher_crud.get_teacher(db, teacher_id)
    if db_teacher is None:
        raise HTTPException(status_code=404, detail="Profesor no encontrado")
    return db_teacher

@app.get("/teachers/", response_model=List[schemas.Teacher])
def read_teachers(db: Session = Depends(get_db)):
    teachers = teacher_crud.get_teachers(db)
    if teachers is None:
        raise HTTPException(status_code=404, detail="Ningún profesor registrado")
    return teachers

@app.post("/teachers/", response_model=schemas.Teacher)
def create_teacher(teacher: schemas.CreateTeacher, db: Session = Depends(get_db)):
    teacher = teacher_crud.create_teacher(db, teacher=teacher)
    if teacher is None:
        raise HTTPException(status_code=404, detail="Ya existe el profesor")
    return teacher

@app.put("/teachers/{teacher_id}", response_model=schemas.Teacher)
def update_teacher(teacher_id: int, teacher: schemas.UpdateTeacher, db: Session = Depends(get_db)):
    new_teacher = teacher_crud.update_teacher(db, teacher_id, teacher.model_dump())
    if new_teacher is None:
        raise HTTPException(status_code=404, detail="Ya existe el profesor")
    return teacher


### Dependenias y endpoints (instruments)

@app.get("/instruments/{instrument_id}", response_model=schemas.Instrument)
def read_instrument(instrument_id: int, db: Session = Depends(get_db)):
    db_instrument = instruments_crud.get_instrument(db, instrument_id)
    if db_instrument is None:
        raise HTTPException(status_code=404, detail="Instrumento no encontrado")
    return db_instrument

@app.get("/instruments/", response_model=List[schemas.Instrument])
def read_instruments(db: Session = Depends(get_db)):
    instruments = instruments_crud.get_all_instruments(db)
    if instruments is None:
        raise HTTPException(status_code=404, detail="Ningún instrumento registrado")
    return instruments

@app.post("/instruments/", response_model=schemas.Instrument)
def create_instrument(instrument: schemas.CreateInstrument, db: Session = Depends(get_db)):
    try:
        new_instrument = instruments_crud.create_instrument(db, name=instrument.name, price=instrument.price)
        return new_instrument
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/instruments/{instrument_id}", response_model=schemas.Instrument)
def update_instrument(instrument_id: int, instrument: schemas.UpdateInstrument, db: Session = Depends(get_db)):
    updated_instrument = instruments_crud.update_instrument(db, instrument_id, name=instrument.name, price=instrument.price)
    if updated_instrument is None:
        raise HTTPException(status_code=404, detail="Instrumento no encontrado")
    return updated_instrument

@app.delete("/instruments/{instrument_id}", response_model=schemas.Instrument)
def delete_instrument(instrument_id: int, db: Session = Depends(get_db)):
    deleted = instruments_crud.delete_instrument(db, instrument_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Instrumento no encontrado")
    return {"message": "Instrumento eliminado correctamente"}

@app.get("/instruments/price-range/", response_model=List[schemas.Instrument])
def read_instruments_by_price_range(min_price: Decimal, max_price: Decimal, db: Session = Depends(get_db)):
    instruments = instruments_crud.get_instruments_by_price_range(db, min_price, max_price)
    if not instruments:
        raise HTTPException(status_code=404, detail="No se encontraron instrumentos en ese rango de precios")
    return instruments