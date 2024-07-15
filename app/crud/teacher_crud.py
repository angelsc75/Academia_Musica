from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
import logging
from models import Teacher
from typing import Optional

# Obtener el logger configurado
logger = logging.getLogger("music_app")

def get_teacher(db: Session, teacher_id: int) -> Teacher:
    try:
        stmt = select(Teacher).where(Teacher.id == teacher_id)
        result = db.scalars(stmt).first()
        if result is None:
            logger.info("Profesor no encontrado")
            raise HTTPException(status_code=404, detail="Profesor no encontrado")
        return result
    except SQLAlchemyError as e:
        logger.error(f"Error de base de datos al obtener el profesor: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        logger.error(f"Error inesperado al obtener el profesor: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

def get_teachers(db: Session):
    try:
        stmt = select(Teacher)
        logger.info("Todos los profesores recuperados con éxito")
        return db.scalars(stmt).all()
    except SQLAlchemyError as e:
        logger.error(f"Error de base de datos al obtener los profesores: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        logger.error(f"Error inesperado al obtener los profesores: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

def create_teacher(db: Session, teacher: Teacher) -> Teacher:
    stmt = select(Teacher).where(
        Teacher.first_name == teacher.first_name,
        Teacher.last_name == teacher.last_name
    )
    result = db.execute(stmt).scalars().first()
    if result is not None:
        logger.info("Profesor ya existente")
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
        logger.info("Profesor creado con éxito")
        return new_teacher
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error de base de datos al crear el profesor: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        db.rollback()
        logger.error(f"Error inesperado al crear el profesor: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

def update_teacher(db: Session, teacher_id: int, new_teacher: dict) -> Teacher:
    try:
        teacher = get_teacher(db, teacher_id)
        for key, value in new_teacher.items():
            if value:
                setattr(teacher, key, value)

        db.commit()
        db.refresh(teacher)
        logger.info("Profesor actualizado con éxito")
        return teacher
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error de base de datos al actualizar el profesor: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except HTTPException as http_exc:
        logger.error(f"HTTPException al actualizar el profesor: {http_exc.detail}")
        raise http_exc
    except Exception as e:
        db.rollback()
        logger.error(f"Error inesperado al actualizar el profesor: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

def delete_teacher(db: Session, teacher_id: int) -> bool:
    try:
        teacher = get_teacher(db, teacher_id)
        db.delete(teacher)
        db.commit()
        logger.info("Profesor eliminado con éxito")
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error de base de datos al eliminar el profesor: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        db.rollback()
        logger.error(f"Error inesperado al eliminar el profesor: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")