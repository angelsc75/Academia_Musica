from sqlalchemy.orm import Session
from decimal import Decimal
from typing import List, Optional
from models import Instrument, Pack, Teacher
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from fastapi import HTTPException
import logging


def create_instrument(db: Session, name: str, price: Decimal) -> Instrument:
    new_instrument = Instrument(name=name, price=price)
    db.add(new_instrument)
    
    try:
        db.commit()
        db.refresh(new_instrument)
        logging.info("Instrumento {new_insturment} creado con éxito")
        return new_instrument
    except IntegrityError:
        # Si hay un error de integridad (por ejemplo, nombre duplicado), revertir los cambios
        db.rollback()
        logging.error(f"Error de integridad al crear el instrumento: {name}")
        raise HTTPException(status_code=400, detail=f"Ya existe un instrumento con el nombre '{name}'")
    except SQLAlchemyError as e:
        db.rollback()
        logging.error(f"Error de base de datos al crear el instrumento: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        db.rollback()
        logging.error(f"Error inesperado al crear el instrumento: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

def get_instrument(db: Session, instrument_id: int) -> Optional[Instrument]:
    try:
        logging.info(f"Instrumento con ID {instrument_id} recuperado con éxito")
        return db.query(Instrument).filter(Instrument.id == instrument_id).first()
    except SQLAlchemyError as e:
        logging.error(f"Error de base de datos al obtener el instrumento con ID {instrument_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        logging.error(f"Error inesperado al obtener el instrumento con ID {instrument_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")


def get_all_instruments(db: Session) -> List[Instrument]:
    try:
        logging.info("Todos los instrumentos recuperados con éxito")
        return db.query(Instrument).all()
    except SQLAlchemyError as e:
        logging.error(f"Error de base de datos al obtener todos los instrumentos: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        logging.error(f"Error inesperado al obtener todos los instrumentos: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

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
                logging.info(f"Instrumento con ID {instrument_id} actualizado con éxito")
                return instrument
            except IntegrityError:
                db.rollback()
                logging.error(f"Error de integridad al actualizar el instrumento: {name}")
                raise HTTPException(status_code=400, detail=f"Ya existe un instrumento con el nombre '{name}'")
        return None
    except SQLAlchemyError as e:
        db.rollback()
        logging.error(f"Error de base de datos al actualizar el instrumento con ID {instrument_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        db.rollback()
        logging.error(f"Error inesperado al actualizar el instrumento con ID {instrument_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

def delete_instrument(db: Session, instrument_id: int) -> bool:
    try:
        instrument = get_instrument(db, instrument_id)
        if instrument:
            db.delete(instrument)
            db.commit()
            logging.info(f"Instrumento con ID {instrument_id} eliminado con éxito")
            return True
        logging.info(f"Instrumento con ID {instrument_id} no encontrado para eliminación")
        return False
    except SQLAlchemyError as e:
        db.rollback()
        logging.error(f"Error de base de datos al eliminar el instrumento con ID {instrument_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        db.rollback()
        logging.error(f"Error inesperado al eliminar el instrumento con ID {instrument_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

def get_instruments_by_price_range(db: Session, min_price: Decimal, max_price: Decimal) -> List[Instrument]:
    try:
        logging.info(f"Instrumentos en el rango de precios {min_price} - {max_price} recuperados con éxito")
        return db.query(Instrument).filter(Instrument.price >= min_price, Instrument.price <= max_price).all()
    except SQLAlchemyError as e:
        logging.error(f"Error de base de datos al obtener instrumentos por rango de precios {min_price} - {max_price}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        logging.error(f"Error inesperado al obtener instrumentos por rango de precios {min_price} - {max_price}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

def get_instruments_by_teacher(db: Session, teacher_id: int) -> List[Instrument]:
    try:
        logging.info(f"Instrumentos asociados al profesor con ID {teacher_id} recuperados con éxito")
        return db.query(Instrument).join(Instrument.teachers).filter(Teacher.id == teacher_id).all()
    except SQLAlchemyError as e:
        logging.error(f"Error de base de datos al obtener instrumentos por profesor con ID {teacher_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        logging.error(f"Error inesperado al obtener instrumentos por profesor con ID {teacher_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

def get_instruments_by_pack(db: Session, pack_id: int) -> List[Instrument]:
    try:
        logging.info(f"Instrumentos asociados al pack con ID {pack_id} recuperados con éxito")
        return db.query(Instrument).join(Instrument.packs).filter(Pack.id == pack_id).all()
    except SQLAlchemyError as e:
        logging.error(f"Error de base de datos al obtener instrumentos por pack con ID {pack_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        logging.error(f"Error inesperado al obtener instrumentos por pack con ID {pack_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")