from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from decimal import Decimal

from db import get_db
from crud.inscriptions_crud import delete_inscription, get_inscriptions, get_inscriptions_by_student, calculate_student_fees, generate_fee_report
from crud.students_crud import get_students, create_student, delete_student, update_student
from crud import teacher_crud, instruments_crud
from crud.levels_crud import create_level, delete_level, update_level, get_levels, get_level
from crud.packs_crud import create_pack, delete_pack, update_pack, get_packs, get_pack
from schemas import Student, StudentCreate, Inscription, InscriptionCreate, InscriptionDetail,\
      FeeReport, Instrument, CreateInstrument, UpdateInstrument, Teacher, CreateTeacher, \
      Level, LevelCreate, LevelUpdate, Pack, PackCreate, PackUpdate, UpdateTeacher


router = APIRouter()

@router.post("/students/", response_model=Student)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    return create_student(db=db, student=student)

@router.get("/students/", response_model=List[Student])
def read_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        students = get_students(db, skip=skip, limit=limit)
        return students
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.put("/students/{student_id}", response_model=Student)
def update_student(student_id: int, student: StudentCreate, db: Session = Depends(get_db)):
    updated_student = update_student(db, student_id, student.dict())
    if updated_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return updated_student

@router.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    success = delete_student(db, student_id)
    if not success:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student deleted successfully"}

@router.post("/inscriptions/", response_model=Inscription)
def create_inscription(inscription: InscriptionCreate, db: Session = Depends(get_db)):
    return create_inscription(db=db, inscription=inscription)

@router.get("/inscriptions/", response_model=List[InscriptionDetail])
def read_inscriptions(db: Session = Depends(get_db)):
    return get_inscriptions(db)

@router.delete("/inscriptions/{inscription_id}")
def delete_inscription_route(inscription_id: int, db: Session = Depends(get_db)):
    result = delete_inscription(db, inscription_id)
    if result:
        return {"message": "Inscription deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Inscription not found")

@router.get("/students/{student_id}/inscriptions", response_model=List[InscriptionDetail])
def read_student_inscriptions(student_id: int, db: Session = Depends(get_db)):
    inscriptions = get_inscriptions_by_student(db, student_id)
    if not inscriptions:
        raise HTTPException(status_code=404, detail="No inscriptions found for this student")
    return inscriptions

@router.get("/students/{student_id}/fee", response_model=float)
def calculate_student_fee(student_id: int, db: Session = Depends(get_db)):
    fee = calculate_student_fees(db, student_id)
    if fee is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return float(fee)

@router.get("/fee_report/", response_model=List[FeeReport])
def get_fee_report(db: Session = Depends(get_db)):
    return generate_fee_report(db)

@router.get("/test/")
def test_endpoint():
    return {"message": "Test endpoint is working"}



@router.get("/teachers/{teacher_id}", response_model=Teacher)
def read_teacher(teacher_id: int, db: Session = Depends(get_db)):
    db_teacher = teacher_crud.get_teacher(db, teacher_id)
    if db_teacher is None:
        raise HTTPException(status_code=404, detail="Profesor no encontrado")
    return db_teacher

@router.get("/teachers/", response_model=List[Teacher])
def read_teachers(db: Session = Depends(get_db)):
    teachers = teacher_crud.get_teachers(db)
    if teachers is None:
        raise HTTPException(status_code=404, detail="Ningún profesor registrado")
    return teachers

@router.post("/teachers/", response_model=Teacher)
def create_teacher(teacher: CreateTeacher, db: Session = Depends(get_db)):
    teacher = teacher_crud.create_teacher(db, teacher=teacher)
    if teacher is None:
        raise HTTPException(status_code=404, detail="Ya existe el profesor")
    return teacher

@router.put("/teachers/{teacher_id}", response_model=Teacher)
def update_teacher(teacher_id: int, teacher: UpdateTeacher, db: Session = Depends(get_db)):
    new_teacher = teacher_crud.update_teacher(db, teacher_id, teacher.model_dump())
    if new_teacher is None:
        raise HTTPException(status_code=404, detail="Ningun profesor con ese id")
    return new_teacher

@router.delete("/teachers/{teacher_id}")
def delete_teacher(teacher_id: int, db: Session = Depends(get_db)):
    if teacher_crud.delete_teacher(db, teacher_id) is False:
        raise HTTPException(status_code=404, detail="Ningun profesor con ese id")
    return {"message": "Profesor eliminado correctamente"}

### Dependenias y endpoints (instruments)

@router.get("/instruments/{instrument_id}", response_model=Instrument)
def read_instrument(instrument_id: int, db: Session = Depends(get_db)):
    db_instrument = instruments_crud.get_instrument(db, instrument_id)
    if db_instrument is None:
        raise HTTPException(status_code=404, detail="Instrumento no encontrado")
    return db_instrument

@router.get("/instruments/", response_model=List[Instrument])
def read_instruments(db: Session = Depends(get_db)):
    instruments = instruments_crud.get_all_instruments(db)
    if instruments is None:
        raise HTTPException(status_code=404, detail="Ningún instrumento registrado")
    return instruments

@router.post("/instruments/", response_model=Instrument)
def create_instrument(instrument: CreateInstrument, db: Session = Depends(get_db)):
    try:
        new_instrument = instruments_crud.create_instrument(db, name=instrument.name, price=instrument.price)
        return new_instrument
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/instruments/{instrument_id}", response_model=Instrument)
def update_instrument(instrument_id: int, instrument: UpdateInstrument, db: Session = Depends(get_db)):
    updated_instrument = instruments_crud.update_instrument(db, instrument_id, name=instrument.name, price=instrument.price)
    if updated_instrument is None:
        raise HTTPException(status_code=404, detail="Instrumento no encontrado")
    return updated_instrument

@router.delete("/instruments/{instrument_id}", response_model=Instrument)
def delete_instrument(instrument_id: int, db: Session = Depends(get_db)):
    deleted = instruments_crud.delete_instrument(db, instrument_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Instrumento no encontrado")
    return {"message": "Instrumento eliminado correctamente"}

@router.get("/instruments/price-range/", response_model=List[Instrument])
def read_instruments_by_price_range(min_price: Decimal, max_price: Decimal, db: Session = Depends(get_db)):
    instruments = instruments_crud.get_instruments_by_price_range(db, min_price, max_price)
    if not instruments:
        raise HTTPException(status_code=404, detail="No se encontraron instrumentos en ese rango de precios")
    return instruments

        

@router.get("/levels/{level_id}", response_model=Level)
def read_level(level_id: int, db: Session = Depends(get_db)):
    db_level = get_level(db, level_id=level_id)
    if db_level is None:
        raise HTTPException(status_code=404, detail="Nivel no encontrado")
    return db_level

@router.get("/levels/", response_model=List[Level])
def read_levels(db: Session = Depends(get_db)):
    return get_levels(db)

@router.post("/levels/", response_model=Level)
def create_level(level: LevelCreate, db: Session = Depends(get_db)):
    db_level = create_level(db, instruments_id=level.instruments_id, level=level.level)
    if db_level is None:
        raise HTTPException(status_code=400, detail="El nivel ya existe")
    return db_level

@router.put("/levels/{level_id}", response_model=Level)
def update_level(level_id: int, level_update: LevelUpdate, db: Session = Depends(get_db)):
    db_level = update_level(db, level_id=level_id, **level_update.dict())
    if db_level is None:
        raise HTTPException(status_code=404, detail="Nivel no encontrado")
    return db_level

@router.delete("/levels/{level_id}", response_model=bool)
def delete_level(level_id: int, db: Session = Depends(get_db)):
    success = delete_level(db, level_id=level_id)
    if not success:
        raise HTTPException(status_code=404, detail="Nivel no encontrado")
    return success

@router.get("/packs/{pack_id}", response_model=Pack)
def read_pack(pack_id: int, db: Session = Depends(get_db)):
    db_pack = get_pack(db, pack_id=pack_id)
    if db_pack is None:
        raise HTTPException(status_code=404, detail="Pack no encontrado")
    return db_pack

@router.get("/packs/", response_model=List[Pack])
def read_packs(db: Session = Depends(get_db)):
    return get_packs(db)

@router.post("/packs/", response_model=Pack)
def create_pack(pack: PackCreate, db: Session = Depends(get_db)):
    db_pack = create_pack(db, pack=pack.pack, discount_1=pack.discount_1, discount_2=pack.discount_2)
    if db_pack is None:
        raise HTTPException(status_code=400, detail="El pack ya existe")
    return db_pack

@router.put("/packs/{pack_id}", response_model=Pack)
def update_pack(pack_id: int, pack_update: PackUpdate, db: Session = Depends(get_db)):
    db_pack = update_pack(db, pack_id=pack_id, **pack_update.dict(exclude_unset=True))
    if db_pack is None:
        raise HTTPException(status_code=404, detail="Pack no encontrado")
    return db_pack

@router.delete("/packs/{pack_id}", response_model=bool)
def delete_pack(pack_id: int, db: Session = Depends(get_db)):
    success = delete_pack(db, pack_id=pack_id)
    if not success:
        raise HTTPException(status_code=404, detail="Pack no encontrado")
    return success