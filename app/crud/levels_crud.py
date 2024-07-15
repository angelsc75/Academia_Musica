from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from typing import Optional, List
from models import Level, Instrument
import logging
''' 
Cada función en este código está diseñada para interactuar con la base de datos a través de SQLAlchemy y manejar las operaciones 
CRUD (crear, leer, actualizar y eliminar) para los niveles (Level). Además, se incluyen manejos de errores detallados y logging para registrar las 
operaciones y posibles fallos.
'''
# Obtener el logger configurado
logger = logging.getLogger("music_app")

# Obtener un nivel específico por ID
def get_level(db: Session, level_id: int) -> Optional[Level]:
    try:
        # Crear una consulta para seleccionar el nivel con el ID especificado
        stmt = select(Level).where(Level.id == level_id)
        # Ejecutar la consulta y obtener el primer resultado
        result = db.scalars(stmt).first()
        if result is None:
            # Si no se encuentra el nivel, registrar un mensaje y lanzar una excepción HTTP 404
            logger.info("Nivel no encontrado")
            raise HTTPException(status_code=404, detail="Nivel no encontrado")
        # Si se encuentra el nivel, registrar un mensaje y devolver el resultado
        logger.info("Nivel recuperado con éxito")
        return result
    except SQLAlchemyError as e:
        # Manejar errores de base de datos, registrar el error y lanzar una excepción HTTP 500
        logger.error(f"Error de base de datos al obtener el nivel: {str(e)}")
        raise HTTPException(status_code=500, detail="Error de base de datos")
    except Exception as e:
        # Manejar otros errores, registrar el error y lanzar una excepción HTTP 500
        logger.error(f"Error inesperado al obtener el nivel: {str(e)}")
        raise HTTPException(status_code=500, detail="Error inesperado")

# Listar todos los niveles
def get_levels(db: Session) -> List[Level]:
    try:
        stmt = select(Level)
        logger.info("Todos los niveles recuperados con éxito")
        return db.scalars(stmt).all()
    except SQLAlchemyError as e:
        logger.error(f"Error de base de datos al obtener los niveles: {str(e)}")
        raise HTTPException(status_code=500, detail="Error de base de datos")
    except Exception as e:
        logger.error(f"Error inesperado al obtener los niveles: {str(e)}")
        raise HTTPException(status_code=500, detail="Error inesperado")

# Crear un nuevo nivel
def create_level(db: Session, instruments_id: int, level: str) -> Optional[Level]:
    try:
        # Verificar si el instrumento existe
        instrument_exists = db.get(Instrument, instruments_id)
        if not instrument_exists:
            logger.info("Instrumento no encontrado")
            raise HTTPException(status_code=404, detail="Instrumento no encontrado")

        # Verificar si ya existe un nivel con el mismo instrumento y nivel
        stmt = select(Level).where(
            (Level.instruments_id == instruments_id) & 
            (Level.level == level)
        )
        result = db.execute(stmt).scalars().first()
        if result:
            logger.info("Nivel ya existente para el instrumento")
            raise HTTPException(status_code=400, detail="Nivel ya existente")

        # Crear un nuevo nivel
        new_level = Level(
            instruments_id=instruments_id,
            level=level
        )
        db.add(new_level)
        db.commit()
        db.refresh(new_level)  # Refrescar la instancia para obtener los datos actualizados de la base de datos
        logger.info("Nivel creado con éxito para el instrumento")
        return new_level
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error de base de datos al crear el nivel: {str(e)}")
        raise HTTPException(status_code=500, detail="Error de base de datos")
    except Exception as e:
        db.rollback()
        logger.error(f"Error inesperado al crear el nivel: {str(e)}")
        raise HTTPException(status_code=500, detail="Error inesperado")

# Actualizar un nivel existente
def update_level(db: Session, level_id: int, **kwargs) -> Optional[Level]:
    try:
        # Verificar si el nivel existe
        level = db.get(Level, level_id)
        if not level:
            logger.info("Nivel no encontrado para actualización")
            raise HTTPException(status_code=404, detail="Nivel no encontrado")

        # Verificar si se actualiza el instrumento y si existe
        if 'instruments_id' in kwargs:
            instrument_exists = db.get(Instrument, kwargs['instruments_id'])
            if not instrument_exists:
                logger.info("Instrumento no encontrado para actualización")
                raise HTTPException(status_code=404, detail="Instrumento no encontrado")

        # Actualizar los campos del nivel
        for key, value in kwargs.items():
            if hasattr(level, key):
                setattr(level, key, value)

        db.commit()
        db.refresh(level)  # Refrescar la instancia para obtener los datos actualizados de la base de datos
        logger.info("Nivel actualizado con éxito")
        return level
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error de base de datos al actualizar el nivel: {str(e)}")
        raise HTTPException(status_code=500, detail="Error de base de datos")
    except Exception as e:
        db.rollback()
        logger.error(f"Error inesperado al actualizar el nivel: {str(e)}")
        raise HTTPException(status_code=500, detail="Error inesperado")

# Eliminar un nivel existente
def delete_level(db: Session, level_id: int) -> bool:
    try:
        level = db.get(Level, level_id)
        if not level:
            logger.info("Nivel no encontrado para eliminación")
            raise HTTPException(status_code=404, detail="Nivel no encontrado")

        db.delete(level)
        db.commit()
        logger.info(f"Nivel con ID {level_id} eliminado con éxito")
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error de base de datos al eliminar el nivel: {str(e)}")
        raise HTTPException(status_code=500, detail="Error de base de datos")
    except Exception as e:
        db.rollback()
        logger.error(f"Error inesperado al eliminar el nivel: {str(e)}")
        raise HTTPException(status_code=500, detail="Error inesperado")