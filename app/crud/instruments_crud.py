from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from decimal import Decimal
from typing import List, Optional


def create_instrument(db: Session, name: str, price: Decimal) -> Instrument:
    # Crear una nueva instancia de Instrument
    new_instrument = Instrument(name=name, price=price)
    
    # Añadir el nuevo instrumento a la sesión
    db.add(new_instrument)
    
    try:
        # Intentar confirmar los cambios en la base de datos
        db.commit()
        # Refrescar el objeto para obtener cualquier valor generado por la base de datos
        db.refresh(new_instrument)
    except IntegrityError:
        # Si hay un error de integridad (por ejemplo, nombre duplicado), revertir los cambios
        db.rollback()
        raise ValueError(f"Ya existe un instrumento con el nombre '{name}'")
    
    return new_instrument

def get_instrument(db: Session, instrument_id: int) -> Optional[Instrument]:
    # Consultar la base de datos para encontrar el instrumento por su ID
    return db.query(Instrument).filter(Instrument.id == instrument_id).first()

def get_all_instruments(db: Session) -> List[Instrument]:
    # Consultar todos los instrumentos en la base de datos
    return db.query(Instrument).all()

def update_instrument(db: Session, instrument_id: int, name: Optional[str] = None, price: Optional[Decimal] = None) -> Optional[Instrument]:
    # Obtener el instrumento de la base de datos
    instrument = get_instrument(db, instrument_id)
    if instrument:
        # Actualizar los campos si se proporcionan nuevos valores
        if name:
            instrument.name = name
        if price is not None:
            instrument.price = price
        
        try:
            # Intentar confirmar los cambios en la base de datos
            db.commit()
            # Refrescar el objeto para obtener cualquier valor actualizado
            db.refresh(instrument)
        except IntegrityError:
            # Si hay un error de integridad (por ejemplo, nombre duplicado), revertir los cambios
            db.rollback()
            raise ValueError(f"Ya existe un instrumento con el nombre '{name}'")
        
        return instrument
    return None

def delete_instrument(db: Session, instrument_id: int) -> bool:
    # Obtener el instrumento de la base de datos
    instrument = get_instrument(db, instrument_id)
    if instrument:
        # Si se encuentra el instrumento, eliminarlo y confirmar los cambios
        db.delete(instrument)
        db.commit()
        return True
    return False

def get_instruments_by_price_range(db: Session, min_price: Decimal, max_price: Decimal) -> List[Instrument]:
    # Consultar instrumentos dentro del rango de precios especificado
    return db.query(Instrument).filter(Instrument.price >= min_price, Instrument.price <= max_price).all()

def get_instruments_by_teacher(db: Session, teacher_id: int) -> List[Instrument]:
    # Consultar instrumentos asociados con el profesor especificado
    return db.query(Instrument).join(Instrument.teachers).filter(Teacher.id == teacher_id).all()

def get_instruments_by_pack(db: Session, pack_id: int) -> List[Instrument]:
    # Consultar instrumentos asociados con el pack especificado
    return db.query(Instrument).join(Instrument.packs).filter(Pack.id == pack_id).all()