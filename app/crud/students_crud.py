from sqlalchemy.orm import Session
from sqlalchemy import and_, select, func
from models import Student, Inscription, Level, Instrument, Pack, PacksInstruments
from schemas import StudentCreate, InscriptionCreate
from typing import List, Dict
from datetime import date
from decimal import Decimal, ROUND_HALF_UP
import logging
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException


def create_student(db: Session, student: StudentCreate):
    try:
        db_student = Student(**student.model_dump())
        db.add(db_student)
        db.commit()
        db.refresh(db_student)
        return db_student
    except SQLAlchemyError as e:
        db.rollback()
        logging.error(f"Error al crear el estudiante: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        db.rollback()
        logging.error(f"Error inesperado al crear el estudiante: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

  
def get_students(db: Session, skip: int = 0, limit: int = 200):
    try:
        students = db.query(Student).offset(skip).limit(limit).all()
        logging.info(f"Retrieved {len(students)} students")
        return students
    except SQLAlchemyError as e:
        logging.error(f"Error de base de datos en get_students: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        logging.error(f"Error inesperado en get_students: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

def get_student(db: Session, student_id: int):
    try:
        stmt = select(Student).where(Student.id == student_id)
        result = db.scalars(stmt).first()
        return result
    except SQLAlchemyError as e:
        logging.error(f"Error de base de datos en get_student: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        logging.error(f"Error inesperado en get_student: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")
    
def update_student(db: Session, student_id: int, student_data: dict):
    try:
        db_student = db.query(Student).filter(Student.id == student_id).first()
        if not db_student:
            raise HTTPException(status_code=404, detail="Estudiante no encontrado")

        for key, value in student_data.items():
            setattr(db_student, key, value)
        db.commit()
        db.refresh(db_student)
        return db_student
    except SQLAlchemyError as e:
        db.rollback()
        logging.error(f"Error de base de datos en update_student: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        db.rollback()
        logging.error(f"Error inesperado en update_student: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")
    
def delete_student(db: Session, student_id: int):
    try:
        db_student = db.query(Student).filter(Student.id == student_id).first()
        if not db_student:
            raise HTTPException(status_code=404, detail="Estudiante no encontrado")

        db.delete(db_student)
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logging.error(f"Error de base de datos en delete_student: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        db.rollback()
        logging.error(f"Error inesperado en delete_student: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")