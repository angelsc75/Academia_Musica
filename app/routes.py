from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from crud import inscriptions_crud
from crud import levels_crud
from crud import packs_crud
from crud import teacher_instruments_crud
from crud import pack_instruments_crud
import schemas
import crud
from core import security
from core.security import create_access_token, decode_access_token, oauth2_scheme
from crud import auth
from models import Student
from schemas import Token
from sqlalchemy.orm import Session
from typing import List
from decimal import Decimal
from db import get_db
from crud.inscriptions_crud import create_inscription, delete_inscription, get_inscriptions, get_inscription, get_inscriptions_by_student, calculate_student_fees, generate_fee_report,update_inscription
from crud.students_crud import get_students, create_student, delete_student, update_student, get_student
from crud import teacher_crud, instruments_crud, students_crud
from crud.levels_crud import create_level, delete_level, update_level, get_levels, get_level
from crud.packs_crud import create_pack, delete_pack, update_pack, get_packs, get_pack
from crud.teacher_instruments_crud import get_teacher_instruments,get_teachers_instruments,update_teachers_instruments,create_teachers_instruments,delete_teacher_instruments
from crud.pack_instruments_crud import create_packs_instruments, delete_packs_instruments, update_packs_instruments, get_pack_instruments, get_packs_instruments
from schemas import Student, StudentCreate, Inscription, InscriptionCreate, InscriptionDetail,\
        FeeReport, Instrument, CreateInstrument, UpdateInstrument, Teacher, CreateTeacher, \
        Level, LevelCreate, LevelUpdate, Pack, PackCreate, PackUpdate, PacksInstruments, PacksInstrumentsCreate, \
        PacksInstrumentsUpdate, TeachersInstruments, TeachersInstrumentsCreate, TeachersInstrumentsUpdate, \
        UpdateTeacher



api_router = APIRouter()
api_router.include_router(auth.router, tags=["authentication"])
api_router.include_router(students_crud.router, prefix="/students", tags=["students"])
api_router.include_router(teacher_crud.router, prefix="/teachers", tags=["teachers"])
api_router.include_router(instruments_crud.router, prefix="/instruments", tags=["instruments"])
api_router.include_router(inscriptions_crud.router, prefix="/inscriptions", tags=["inscriptions"])
api_router.include_router(levels_crud.router, prefix="/levels", tags=["levels"])
api_router.include_router(packs_crud.router, prefix="/packs", tags=["packs"])
api_router.include_router(teacher_instruments_crud.router, prefix="/teacher-instruments", tags=["teacher_instruments"])
api_router.include_router(pack_instruments_crud.router, prefix="/pack-instruments", tags=["pack_instruments"])



router = APIRouter()

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/students/", response_model=Student, tags=["students"])
def create_students(student: StudentCreate, db: Session = Depends(get_db)):
    return create_student(db=db, student=student)

@router.get("/students/{student_id}", response_model=Student, tags=["students"])
def read_student(student_id: int, db: Session = Depends(get_db)):
    db_student = students_crud.get_student(db, student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    return db_student

@router.get("/students/", response_model=List[Student], tags=["students"])
def read_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        students = get_students(db, skip=skip, limit=limit)
        return students
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.put("/students/{student_id}", response_model=Student, tags=["students"])
def update_students(student_id: int, student: StudentCreate, db: Session = Depends(get_db)):
    updated_student = update_student(db, student_id, student.model_dump())
    if updated_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return updated_student

@router.delete("/students/{student_id}", tags=["students"])
def delete_students(student_id: int, db: Session = Depends(get_db)):
    success = delete_student(db, student_id)
    if not success:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student deleted successfully"}

@router.post("/inscriptions/", response_model=Inscription, tags=["inscriptions"])
def create_inscriptions(inscription: InscriptionCreate, db: Session = Depends(get_db)):
    return create_inscription(db=db, inscription=inscription)

@router.get("/inscriptions/", response_model=List[InscriptionDetail], tags=["inscriptions"])
def read_inscriptions(db: Session = Depends(get_db)):
    return get_inscriptions(db)

@router.get("/inscriptions/{inscription_id}", response_model=Inscription, tags=["inscriptions"])
def read_inscription(inscription_id: int, db: Session = Depends(get_db)):
    db_inscription = get_inscription(db, inscription_id)
    if db_inscription is None:
        raise HTTPException(status_code=404, detail="Inscripción  no encontrada")
    return db_inscription

@router.delete("/inscriptions/{inscription_id}", tags=["inscriptions"])
def delete_inscription_route(inscription_id: int, db: Session = Depends(get_db)):
    result = delete_inscription(db, inscription_id)
    if result:
        return {"message": "Inscription deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Inscription not found")
    
@router.put("/inscriptions/{inscription_id}", response_model=Inscription, tags=["inscriptions"])
def update_inscriptions(inscription_id: int, inscription: InscriptionCreate, db: Session = Depends(get_db)):
    updated_inscription = update_inscription(db, inscription_id, inscription.model_dump())
    if updated_inscription is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return updated_inscription

@router.get("/students/{student_id}/inscriptions", response_model=List[InscriptionDetail], tags=["inscriptions by student"])
def read_student_inscriptions(student_id: int, db: Session = Depends(get_db)):
    inscriptions = get_inscriptions_by_student(db, student_id)
    if not inscriptions:
        raise HTTPException(status_code=404, detail="No inscriptions found for this student")
    return inscriptions

@router.get("/students/{student_id}/fee", response_model=float, tags=["fees"])
def calculate_student_fee(student_id: int, db: Session = Depends(get_db)):
    fee = calculate_student_fees(db, student_id)
    if fee is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return float(fee)

@router.get("/fee_report/", response_model=List[FeeReport], tags=["fees"])
def get_fee_report(db: Session = Depends(get_db)):
    return generate_fee_report(db)

@router.get("/test/", tags=["test"])
def test_endpoint():
    return {"message": "Test endpoint is working"}



@router.get("/teachers/{teacher_id}", response_model=Teacher, tags=["teachers"])
def read_teacher(teacher_id: int, db: Session = Depends(get_db)):
    db_teacher = teacher_crud.get_teacher(db, teacher_id)
    if db_teacher is None:
        raise HTTPException(status_code=404, detail="Profesor no encontrado")
    return db_teacher

@router.get("/teachers/", response_model=List[Teacher], tags=["teachers"])
def read_teachers(db: Session = Depends(get_db)):
    teachers = teacher_crud.get_teachers(db)
    if teachers is None:
        raise HTTPException(status_code=404, detail="Ningún profesor registrado")
    return teachers

@router.post("/teachers/", response_model=Teacher, tags=["teachers"])
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

@router.get("/instruments/{instrument_id}", response_model=Instrument, tags=["instruments"])
def read_instrument(instrument_id: int, db: Session = Depends(get_db)):
    db_instrument = instruments_crud.get_instrument(db, instrument_id)
    if db_instrument is None:
        raise HTTPException(status_code=404, detail="Instrumento no encontrado")
    return db_instrument

@router.get("/instruments/", response_model=List[Instrument], tags=["instruments"])
def read_instruments(db: Session = Depends(get_db)):
    instruments = instruments_crud.get_all_instruments(db)
    if instruments is None:
        raise HTTPException(status_code=404, detail="Ningún instrumento registrado")
    return instruments

@router.post("/instruments/", response_model=Instrument, tags=["instruments"])
def create_instrument(instrument: CreateInstrument, db: Session = Depends(get_db)):
    try:
        new_instrument = instruments_crud.create_instrument(db, name=instrument.name, price=instrument.price)
        return new_instrument
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/instruments/{instrument_id}", response_model=Instrument, tags=["instruments"])
def update_instrument(instrument_id: int, instrument: UpdateInstrument, db: Session = Depends(get_db)):
    updated_instrument = instruments_crud.update_instrument(db, instrument_id, name=instrument.name, price=instrument.price)
    if updated_instrument is None:
        raise HTTPException(status_code=404, detail="Instrumento no encontrado")
    return updated_instrument

@router.delete("/instruments/{instrument_id}", response_model=Instrument, tags=["instruments"])
def delete_instrument(instrument_id: int, db: Session = Depends(get_db)):
    deleted = instruments_crud.delete_instrument(db, instrument_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Instrumento no encontrado")
    return {"message": "Instrumento eliminado correctamente"}

@router.get("/instruments/price-range/", response_model=List[Instrument], tags=["instruments"])
def read_instruments_by_price_range(min_price: Decimal, max_price: Decimal, db: Session = Depends(get_db)):
    instruments = instruments_crud.get_instruments_by_price_range(db, min_price, max_price)
    if not instruments:
        raise HTTPException(status_code=404, detail="No se encontraron instrumentos en ese rango de precios")
    return instruments

        

@router.get("/levels/{level_id}", response_model=Level, tags=["levels"])
def read_level(level_id: int, db: Session = Depends(get_db)):
    db_level = get_level(db, level_id=level_id)
    if db_level is None:
        raise HTTPException(status_code=404, detail="Nivel no encontrado")
    return db_level

@router.get("/levels/", response_model=List[Level], tags=["levels"])
def read_levels(db: Session = Depends(get_db)):
    return get_levels(db)

@router.post("/levels/", response_model=Level, tags=["levels"])
def create_levels(level: LevelCreate, db: Session = Depends(get_db)):
    db_level = create_level(db, instruments_id=level.instruments_id, level=level.level)
    if db_level is None:
        raise HTTPException(status_code=400, detail="El nivel ya existe")
    return db_level

@router.put("/levels/{level_id}", response_model=Level, tags=["levels"])
def update_level(level_id: int, level_update: LevelUpdate, db: Session = Depends(get_db)):
    db_level = update_level(db, level_id=level_id, **level_update.model_dump())
    if db_level is None:
        raise HTTPException(status_code=404, detail="Nivel no encontrado")
    return db_level

@router.delete("/levels/{level_id}", response_model=bool, tags=["levels"])
def delete_level(level_id: int, db: Session = Depends(get_db)):
    success = delete_level(db, level_id=level_id)
    if not success:
        raise HTTPException(status_code=404, detail="Nivel no encontrado")
    return success

@router.get("/packs/{pack_id}", response_model=Pack, tags=["packs"])
def read_pack(pack_id: int, db: Session = Depends(get_db)):
    db_pack = get_pack(db, pack_id=pack_id)
    if db_pack is None:
        raise HTTPException(status_code=404, detail="Pack no encontrado")
    return db_pack

@router.get("/packs/", response_model=List[Pack], tags=["packs"])
def read_packs(db: Session = Depends(get_db)):
    return get_packs(db)

@router.post("/packs/", response_model=Pack, tags=["packs"])
def create_packs(pack: PackCreate, db: Session = Depends(get_db)):
    db_pack = create_pack(db, pack=pack.pack, discount_1=pack.discount_1, discount_2=pack.discount_2)
    if db_pack is None:
        raise HTTPException(status_code=400, detail="El pack ya existe")
    return db_pack

@router.put("/packs/{pack_id}", response_model=Pack, tags=["packs"])
def update_packs(pack_id: int, pack_update: PackUpdate, db: Session = Depends(get_db)):
    db_pack = update_pack(db, pack_id=pack_id, **pack_update.model_dump(exclude_unset=True))
    if db_pack is None:
        raise HTTPException(status_code=404, detail="Pack no encontrado")
    return db_pack

@router.delete("/packs/{pack_id}", response_model=bool, tags=["packs"])
def delete_packs(pack_id: int, db: Session = Depends(get_db)):
    success = delete_pack(db, pack_id=pack_id)
    if not success:
        raise HTTPException(status_code=404, detail="Pack no encontrado")
    return success


@router.get("/packs_instruments/{packs_instruments_id}", response_model=PacksInstruments, tags=["packs_instruments"])
def read_pack_instruments(packs_instruments_id: int, db: Session = Depends(get_db)):
    db_packs_instruments = get_pack_instruments(db, packs_instruments_id=packs_instruments_id)
    if db_packs_instruments is None:
        raise HTTPException(status_code=404, detail="Pack de instrumentos no encontrado")
    return db_packs_instruments

@router.get("/packs_instruments/", response_model=List[PacksInstruments], tags=["packs_instruments"])
def read_packs_instruments(db: Session = Depends(get_db)):
    return get_packs_instruments(db)

@router.post("/packs_instruments/", response_model=PacksInstruments, tags=["packs_instruments"])
def create_pack_instruments(packs_instruments: PacksInstrumentsCreate, db: Session = Depends(get_db)):
    db_pack_instruments = create_packs_instruments(db, packs_instruments_id=packs_instruments.pack_instruments_id, packs_id=packs_instruments.pack_id, instrument_id=packs_instruments.instrument_id)
    if db_pack_instruments is None:
        raise HTTPException(status_code=400, detail="El pack de instrumentos ya existe")
    return db_pack_instruments

@router.put("/packs_instruments/{packs_instruments_id}", response_model=PacksInstruments, tags=["packs_instruments"])
def update_pack_instrument(packs_instruments_id: int, packs_instruments_update: PacksInstrumentsUpdate, db: Session = Depends(get_db)):
    db_packs_instrument = update_packs_instruments(db, packs_instrument_id=packs_instruments_id, packs_instruments_update=packs_instruments_update)
    if db_packs_instrument is None:
        raise HTTPException(status_code=404, detail="Pack de instrumentos no encontrado")
    return db_packs_instrument

@router.delete("/packs_instruments/{pack_instrument_id}", response_model=bool, tags=["packs_instruments"])
def delete_pack_instrument(pack_instrument_id: int, db: Session = Depends(get_db)):
    success = delete_pack(db, pack_instrument_id=pack_instrument_id)
    if not success:
        raise HTTPException(status_code=404, detail="Pack no encontrado")
    return success

@router.get("/teachers_instruments/{teachers_instruments_id}", response_model=TeachersInstruments, tags=["teachers_instruments"])
def read_teachers_instruments(teachers_instruments_id: int, db: Session = Depends(get_db)):
    db_teachers_instruments = get_teacher_instruments(db, teachers_instruments_id=teachers_instruments_id)
    if db_teachers_instruments is None:
        raise HTTPException(status_code=404, detail="Relación de profesor e instrumento no encontrada")
    return db_teachers_instruments

@router.get("/teachers_instruments/", response_model=List[TeachersInstruments], tags=["teachers_instruments"])
def read_teachers_instruments(db: Session = Depends(get_db)):
    return get_teachers_instruments(db)

@router.post("/teachers_instruments/", response_model=TeachersInstruments, tags=["teachers_instruments"])
def create_teacher_instrument(teachers_instruments: TeachersInstrumentsCreate, db: Session = Depends(get_db)):
    db_teachers_instruments = create_teachers_instruments(db, teachers_instruments_id = teachers_instruments.teachers_instruments_id, teacher_id=teachers_instruments.teacher_id, instrument_id=teachers_instruments.instrument_id)
    if db_teachers_instruments is None:
        raise HTTPException(status_code=400, detail="La asociación de profesor e instrumento ya existe")
    return db_teachers_instruments

@router.put("/teachers_instruments/{teachers_instruments_id}", response_model=TeachersInstruments, tags=["teachers_instruments"])
def update_teachers_instrument(teachers_instruments_id: int, teachers_instruments_update: TeachersInstrumentsUpdate, db: Session = Depends(get_db)):
    db_teachers_instruments = update_teachers_instruments(db, teachers_isntruments_id=teachers_instruments_id, **teachers_instruments_update.model_dump(exclude_unset=True))
    if db_teachers_instruments is None:
        raise HTTPException(status_code=404, detail="Asociación de profesor e instrumento no encontrada")
    return db_teachers_instruments

@router.delete("/teachers_instruments/{teachers_instruments_id}", response_model=bool, tags=["teachers_instruments"])
def delete_teachers_instrument(teachers_instruments_id: int, db: Session = Depends(get_db)):
    success = delete_pack(db, teachers_instruments_id=teachers_instruments_id)
    if not success:
        raise HTTPException(status_code=404, detail="Asociación de profesor e instrumento no encontrada")
    return success
def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload

@router.get("/", response_model=list[schemas.Student])
def read_students(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db), 
    current_user: schemas.User = Depends(security.get_current_active_user)
):
    students = crud.get_students(db, skip=skip, limit=limit)
    return students