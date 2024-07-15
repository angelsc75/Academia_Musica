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

# Obtener el logger configurado
logger = logging.getLogger("music_app")

def create_student(db: Session, student: StudentCreate):
    try:
        db_student = Student(**student.model_dump())
        db.add(db_student)
        db.commit()
        db.refresh(db_student)
        logger.info("Estudiante creado con éxito")
        return db_student
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error al crear el estudiante: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        db.rollback()
        logger.error(f"Error inesperado al crear el estudiante: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

def get_students(db: Session, skip: int = 0, limit: int = 200):
    try:
        students = db.query(Student).offset(skip).limit(limit).all()
        logger.info(f"Recuperados {len(students)} estudiantes")
        return students
    except SQLAlchemyError as e:
        logger.error(f"Error de base de datos recuperando estudiantes: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        logger.error(f"Error inesperado recuperando estudiantes: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

def get_student(db: Session, student_id: int):
    try:
        stmt = select(Student).where(Student.id == student_id)
        result = db.scalars(stmt).first()
        logger.info("Estudiante recuperado con éxito")
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error de base de datos recuperando estudiante: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        logger.error(f"Error inesperado en recuperando estudiante: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")
    
def update_student(db: Session, student_id: int, student_data: dict):
    try:
        db_student = db.query(Student).filter(Student.id == student_id).first()
        if not db_student:
            logger.info("Estudiante no encontrado")
            raise HTTPException(status_code=404, detail="Estudiante no encontrado")

        for key, value in student_data.items():
            setattr(db_student, key, value)
        db.commit()
        db.refresh(db_student)
        logger.info("Estudiante actualizado con éxito")
        return db_student
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error de base de datos al actualizar estudiante: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except HTTPException as http_exc:
        logger.error(f"HTTPException al actualizar estudiante: {http_exc.detail}")
        raise http_exc
    except Exception as e:
        db.rollback()
        logger.error(f"Error inesperado al actualizar estudiante: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")
    
def delete_student(db: Session, student_id: int):
    try:
        db_student = db.query(Student).filter(Student.id == student_id).first()
        if not db_student:
            logger.info("Estudiante no encontrado")
            raise HTTPException(status_code=404, detail="Estudiante no encontrado")

        db.delete(db_student)
        db.commit()
        logger.info("Estudiante eliminado con éxito")
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error de base de datos al eliminar al estudiante: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except HTTPException as http_exc: 
        logger.error(f"HTTPException al eliminar: {http_exc.detail}")
        raise http_exc
    except Exception as e:
        db.rollback()
        logger.error(f"Error inesperado al eliminar el estudiante: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")