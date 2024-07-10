from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
import crud
from schemas import Student, StudentCreate, Inscription, InscriptionCreate, InscriptionDetail, FeeReport

router = APIRouter()

@router.post("/students/", response_model=Student)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    return crud.create_student(db=db, student=student)

@router.get("/students/", response_model=List[Student])
def read_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    students = crud.get_students(db, skip=skip, limit=limit)
    return students

@router.get("/students/", response_model=List[Student])
def read_students(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        students = crud.get_students(db, skip=skip, limit=limit)
        return students
    except Exception as e:
        logging.error(f"Error in read_students: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    
@router.put("/students/{student_id}", response_model=Student)
def update_student(student_id: int, student: StudentCreate, db: Session = Depends(get_db)):
    updated_student = crud.update_student(db, student_id, student.dict())
    if updated_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return updated_student

@router.delete("/students/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    success = crud.delete_student(db, student_id)
    if not success:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student deleted successfully"}

@router.post("/inscriptions/", response_model=Inscription)
def create_inscription(inscription: InscriptionCreate, db: Session = Depends(get_db)):
    return crud.create_inscription(db=db, inscription=inscription)

@router.get("/inscriptions/", response_model=List[InscriptionDetail])
def read_inscriptions(db: Session = Depends(get_db)):
    return crud.get_inscriptions(db)

@router.get("/students/{student_id}/fee", response_model=float)
def calculate_student_fee(student_id: int, db: Session = Depends(get_db)):
    fee = crud.calculate_student_fees(db, student_id)
    if fee is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return float(fee)

@router.get("/fee_report/", response_model=List[FeeReport])
def get_fee_report(db: Session = Depends(get_db)):
    return crud.generate_fee_report(db)

@router.get("/test/")
def test_endpoint():
    return {"message": "Test endpoint is working"}
