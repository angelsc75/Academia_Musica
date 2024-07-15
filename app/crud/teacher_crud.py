from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
import logging
from models import Teacher
from typing import Optional

def get_teacher(db: Session, teacher_id: int) -> Teacher:
    try:
        stmt = select(Teacher).where(Teacher.id == teacher_id)
        result = db.scalars(stmt).first()
        if result is None:
            logging.info(f"Profesor con ID {teacher_id} no encontrado")
            raise HTTPException(status_code=404, detail="Profesor no encontrado")
        return result
    except SQLAlchemyError as e:
        logging.error(f"Error de base de datos al obtener el profesor con ID {teacher_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        logging.error(f"Error inesperado al obtener el profesor con ID {teacher_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

def get_teachers(db: Session):
    try:
        stmt = select(Teacher)
        logging.info("Todos los profesores recuperados con éxito")
        return db.scalars(stmt).all()
    except SQLAlchemyError as e:
        logging.error(f"Error de base de datos al obtener los profesores: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        logging.error(f"Error inesperado al obtener los profesores: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

def create_teacher(db: Session, teacher: Teacher) -> Teacher:
    stmt = select(Teacher).where(
        Teacher.first_name == teacher.first_name,
        Teacher.last_name == teacher.last_name
    )
    result = db.execute(stmt).scalars().first()
    if result is not None:
        logging.info(f"Profesor ya existente: {teacher.first_name} {teacher.last_name}")
        raise HTTPException(status_code=400, detail="Profesor ya existente")

    new_teacher = Teacher(
        first_name=teacher.first_name,
        last_name=teacher.last_name,
        phone=teacher.phone,
        mail=teacher.mail
    )
    db.add(new_teacher)

    try:
        db.commit()
        db.refresh(new_teacher)
        logging.info(f"Profesor creado con éxito: {new_teacher.first_name} {new_teacher.last_name}")
        return new_teacher
    except SQLAlchemyError as e:
        db.rollback()
        logging.error(f"Error de base de datos al crear el profesor: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        db.rollback()
        logging.error(f"Error inesperado al crear el profesor: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

def update_teacher(db: Session, teacher_id: int, new_teacher: dict) -> Teacher:
    try:
        teacher = get_teacher(db, teacher_id)
        for key, value in new_teacher.items():
            if value:
                setattr(teacher, key, value)

        db.commit()
        db.refresh(teacher)
        logging.info(f"Profesor con ID {teacher_id} actualizado con éxito")
        return teacher
    except SQLAlchemyError as e:
        db.rollback()
        logging.error(f"Error de base de datos al actualizar el profesor con ID {teacher_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos con ID {teacher_id}: {str(e)}")
    except HTTPException as http_exc:
        logging.error(f"HTTPException al actualizar el profesor con ID {teacher_id}: {http_exc.detail}")
        raise http_exc
    except Exception as e:
        db.rollback()
        logging.error(f"Error inesperado al actualizar el profesor con ID {teacher_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

def delete_teacher(db: Session, teacher_id: int) -> bool:
    try:
        teacher = get_teacher(db, teacher_id)
        db.delete(teacher)
        db.commit()
        logging.info(f"Profesor con ID {teacher_id} eliminado con éxito")
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logging.error(f"Error de base de datos al eliminar el profesor con ID {teacher_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        db.rollback()
        logging.error(f"Error inesperado al eliminar el profesor con ID {teacher_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")