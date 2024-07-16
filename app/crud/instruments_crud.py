from sqlalchemy.orm import Session
from decimal import Decimal
from typing import List, Optional
from models import Instrument, Pack, Teacher
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from fastapi import HTTPException
import logging


'''
Cada función en este código está diseñada para interactuar con la base de datos a través de SQLAlchemy y manejar las operaciones 
CRUD (crear, leer, actualizar y eliminar) para los instrumentos (Instrument). Además, se incluyen manejos de errores detallados y 
logging para registrar las operaciones y posibles fallos.
'''
# Obtener el logger configurado
logger = logging.getLogger("music_app")

# Crear un nuevo instrumento
def create_instrument(db: Session, name: str, price: Decimal) -> Instrument:
    # Comprobar si el instrumento ya existe
    existing_instrument = db.query(Instrument).filter((Instrument.name) == (name).lower()).first()
    if existing_instrument:
        logger.warning(f"Intento de crear un instrumento que ya existe: {name}")
        raise HTTPException(status_code=400, detail=f"Ya existe un instrumento con el nombre '{name}'")

    # Crear el nuevo instrumento
    new_instrument = Instrument(name=name, price=price)
    db.add(new_instrument)
    
    try:
        db.commit()
        db.refresh(new_instrument)
        logger.info("Instrumento creado con éxito")
        return new_instrument
    except IntegrityError:
        # Si hay un error de integridad (por ejemplo, nombre duplicado), revertir los cambios
        db.rollback()
        logger.error(f"Error de integridad al crear el instrumento: {name}")
        raise HTTPException(status_code=400, detail=f"Ya existe un instrumento con el nombre '{name}'")
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error de base de datos al crear el instrumento: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        db.rollback()
        logger.error(f"Error inesperado al crear el instrumento: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

# Consultar instrumento por ID
def get_instrument(db: Session, instrument_id: int) -> Optional[Instrument]:
    try:
        logger.info("Instrumento recuperado con éxito")
        return db.query(Instrument).filter(Instrument.id == instrument_id).first()
    except SQLAlchemyError as e:
        logger.error(f"Error de base de datos al obtener el instrumento: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        logger.error(f"Error inesperado al obtener el instrumento: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

# Consultar todos los instrumentos
def get_all_instruments(db: Session) -> List[Instrument]:
    try:
        logger.info("Todos los instrumentos recuperados con éxito")
        return db.query(Instrument).all()
    except SQLAlchemyError as e:
        logger.error(f"Error de base de datos al obtener todos los instrumentos: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        logger.error(f"Error inesperado al obtener todos los instrumentos: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

# Actualizar un instrumento
def update_instrument(db: Session, instrument_id: int, name: Optional[str] = None, price: Optional[Decimal] = None) -> Optional[Instrument]:
    try:
        instrument = get_instrument(db, instrument_id)
        if instrument:
            if name:
                instrument.name = name
            if price is not None:
                instrument.price = price
            
            try:
                db.commit()
                db.refresh(instrument)
                logger.info("Instrumento actualizado con éxito")
                return instrument
            except IntegrityError:
                db.rollback()
                logger.error(f"Error de integridad al actualizar el instrumento: {name}")
                raise HTTPException(status_code=400, detail=f"Ya existe un instrumento con el nombre '{name}'")
        return None
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error de base de datos al actualizar el instrumento: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        db.rollback()
        logger.error(f"Error inesperado al actualizar el instrumento: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

# Eliminar un instrumento
def delete_instrument(db: Session, instrument_id: int) -> bool:
    try:
        instrument = get_instrument(db, instrument_id)
        if instrument:
            db.delete(instrument)
            db.commit()
            logger.info("Instrumento eliminado con éxito")
            return True
        logger.info("Instrumento no encontrado para eliminación")
        return False
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error de base de datos al eliminar el instrumento: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        db.rollback()
        logger.error(f"Error inesperado al eliminar el instrumento: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

# Consultar instrumentos por rango de precios
def get_instruments_by_price_range(db: Session, min_price: Decimal, max_price: Decimal) -> List[Instrument]:
    try:
        logger.info(f"Instrumentos en el rango de precios {min_price} - {max_price} recuperados con éxito")
        return db.query(Instrument).filter(Instrument.price >= min_price, Instrument.price <= max_price).all()
    except SQLAlchemyError as e:
        logger.error(f"Error de base de datos al obtener instrumentos por rango de precios {min_price} - {max_price}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        logger.error(f"Error inesperado al obtener instrumentos por rango de precios {min_price} - {max_price}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

# Consultar instrumentos por profesor
def get_instruments_by_teacher(db: Session, teacher_id: int) -> List[Instrument]:
    try:
        logger.info("Instrumentos por profesor recuperados con éxito")
        return db.query(Instrument).join(Instrument.teachers).filter(Teacher.id == teacher_id).all()
    except SQLAlchemyError as e:
        logger.error(f"Error de base de datos al obtener instrumentos por profesor: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        logger.error(f"Error inesperado al obtener instrumentos por profesor: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

# Consultar instrumentos por pack
def get_instruments_by_pack(db: Session, pack_id: int) -> List[Instrument]:
    try:
        logger.info("Instrumentos asociados al pack recuperados con éxito")
        return db.query(Instrument).join(Instrument.packs).filter(Pack.id == pack_id).all()
    except SQLAlchemyError as e:
        logger.error(f"Error de base de datos al obtener instrumentos por pack: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        logger.error(f"Error inesperado al obtener instrumentos por pack: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")