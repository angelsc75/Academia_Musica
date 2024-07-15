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
        return db.query(Instrument).filter(Instrument.id == instrument_id).first()
    except SQLAlchemyError as e:
        logging.error(f"Error de base de datos al obtener el instrumento: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        logging.error(f"Error inesperado al obtener el instrumento: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")


def get_all_instruments(db: Session) -> List[Instrument]:
    try:
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
                return instrument
            except IntegrityError:
                db.rollback()
                logging.error(f"Error de integridad al actualizar el instrumento: {name}")
                raise HTTPException(status_code=400, detail=f"Ya existe un instrumento con el nombre '{name}'")
        return None
    except SQLAlchemyError as e:
        db.rollback()
        logging.error(f"Error de base de datos al actualizar el instrumento: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        db.rollback()
        logging.error(f"Error inesperado al actualizar el instrumento: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

def delete_instrument(db: Session, instrument_id: int) -> bool:
    try:
        instrument = get_instrument(db, instrument_id)
        if not instrument:
            raise HTTPException(status_code=404, detail="Instrumento no encontrado")

        db.delete(instrument)
        db.commit()
        return True
    except HTTPException as e:
        logging.error(f"Error HTTP al eliminar el instrumento: {str(e)}")
        raise
    except SQLAlchemyError as e:
        db.rollback()
        logging.error(f"Error de base de datos al eliminar el instrumento: {str(e)}")
        raise HTTPException(status_code=500, detail="Error de base de datos")
    except Exception as e:
        db.rollback()
        logging.error(f"Error inesperado al eliminar el instrumento: {str(e)}")
        raise HTTPException(status_code=500, detail="Error inesperado")

def get_instruments_by_price_range(db: Session, min_price: Decimal, max_price: Decimal) -> List[Instrument]:
    try:
        return db.query(Instrument).filter(Instrument.price >= min_price, Instrument.price <= max_price).all()
    except SQLAlchemyError as e:
        logging.error(f"Error de base de datos al obtener instrumentos por rango de precios: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        logging.error(f"Error inesperado al obtener instrumentos por rango de precios: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

def get_instruments_by_teacher(db: Session, teacher_id: int) -> List[Instrument]:
    try:
        return db.query(Instrument).join(Instrument.teachers).filter(Teacher.id == teacher_id).all()
    except SQLAlchemyError as e:
        logging.error(f"Error de base de datos al obtener instrumentos por profesor: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        logging.error(f"Error inesperado al obtener instrumentos por profesor: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

def get_instruments_by_pack(db: Session, pack_id: int) -> List[Instrument]:
    try:
        return db.query(Instrument).join(Instrument.packs).filter(Pack.id == pack_id).all()
    except SQLAlchemyError as e:
        logging.error(f"Error de base de datos al obtener instrumentos por pack: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        logging.error(f"Error inesperado al obtener instrumentos por pack: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")