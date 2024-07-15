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
        logging.info("Estudiante creado {db_student} con éxito")
        return db_student
    except SQLAlchemyError as e:
        db.rollback()
        logging.error(f"Error al crear el estudiante {db_student}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        db.rollback()
        logging.error(f"Error inesperado al crear el estudiante {db_student}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

def get_students(db: Session, skip: int = 0, limit: int = 200):
    try:
        students = db.query(Student).offset(skip).limit(limit).all()
        logging.info(f"Recuperados {len(students)} students")
        return students
    except SQLAlchemyError as e:
        logging.error(f"Error de base de datos recuperando estudiantes: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        logging.error(f"Error inesperado recuperando estudiantes: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

def get_student(db: Session, student_id: int):
    try:
        stmt = select(Student).where(Student.id == student_id)
        result = db.scalars(stmt).first()
        logging.info(f"Estudiante {result} recuperado con éxito")
        return result
    except SQLAlchemyError as e:
        logging.error(f"Error de base de datos recuperando estudiante {result}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        logging.error(f"Error inesperado en recuperando estudiante {result}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")
    
def update_student(db: Session, student_id: int, student_data: dict):
    try:
        logging.info(f"Iniciando actualización del estudiante con ID: {student_id}")
        db_student = db.query(Student).filter(Student.id == student_id).first()
        if not db_student:
            logging.info(f"Estudiante con ID {student_id} no encontrado")
            raise HTTPException(status_code=404, detail="Estudiante no encontrado")

        for key, value in student_data.items():
            setattr(db_student, key, value)
        db.commit()
        db.refresh(db_student)
        logging.info(f"Estudiante con ID {student_id} actualizado con éxito")
        return db_student
    except SQLAlchemyError as e:
        db.rollback()
        logging.error(f"Error de base de datos al actualizar estudiante con ID {student_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except HTTPException as http_exc:
        logging.error(f"HTTPException al actualizar estudiante con ID {student_id}: {http_exc.detail}")
        raise http_exc
    except Exception as e:
        db.rollback()
        logging.error(f"Error inesperado al actualizar estudiante con ID {student_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")
    
def delete_student(db: Session, student_id: int):
    try:
        logging.info(f"Iniciando eliminación del estudiante con ID: {student_id}")
        db_student = db.query(Student).filter(Student.id == student_id).first()
        if not db_student:
            logging.info(f"Estudiante con ID {student_id} no encontrado")
            raise HTTPException(status_code=404, detail="Estudiante no encontrado")

        db.delete(db_student)
        db.commit()
        logging.info(f"Estudiante con ID {student_id} eliminado con éxito")
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logging.error(f"Error de base de datos al eliminar al estudiante con ID {student_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except HTTPException as http_exc: 
        logging.error(f"HTTPException al eliminar al estudiante con ID {student_id}: {http_exc.detail}")
        raise http_exc
    except Exception as e:
        db.rollback()
        logging.error(f"Error inesperado al eliminar al estudiante con ID {student_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")