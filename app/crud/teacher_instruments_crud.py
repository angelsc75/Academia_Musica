from sqlalchemy import select
from sqlalchemy.orm import Session

from models import TeachersInstruments, Instrument, Teacher

def get_teacher_instruments(db: Session, teachers_instruments_id: int):
    stmt = select(TeachersInstruments).where(TeachersInstruments.id == teachers_instruments_id)
    result = db.scalars(stmt).first()
    return result

# Listar todas las relaciones de profesor-instrumento
def get_teachers_instruments(db: Session):
	stmt = select(TeachersInstruments)
	return db.scalars(stmt).all()

# Crear un nuevo nivel
def create_teachers_instruments(db: Session, teacher_id: int, instrument_id: int):
    # Verificar si ya existe un nivel con el mismo instrumento y nivel
    stmt = select(TeachersInstruments).where(
        (TeachersInstruments.instrument_id == instrument_id) &
        (TeachersInstruments.teacher_id == teacher_id)
    )
    result = db.execute(stmt).scalars().first()
    if result:
        return None  # Nivel ya existente

    # Crear un nuevo nivel
    new_teachers_instruments = TeachersInstruments(
        teacher_id=teacher_id,
        instrument_id=instrument_id
    )
    db.add(new_teachers_instruments)
    db.commit()
    db.refresh(new_teachers_instruments)  # Refrescar la instancia para obtener los datos actualizados de la base de datos
    return new_teachers_instruments

def update_teachers_instruments(db: Session, teachers_instruments_id: int, **kwargs):
    # Verificar si el nivel existe
    teachers_instruments = db.get(TeachersInstruments, teachers_instruments_id)
    if not teachers_instruments:
        return None  # Nivel no encontrado

    # Actualizar los campos del nivel
    for key, value in kwargs.items():
        if hasattr(teachers_instruments, key):
            setattr(teachers_instruments, key, value)

    db.commit()
    db.refresh(teachers_instruments)  # Refrescar la instancia para obtener los datos actualizados de la base de datos
    return teachers_instruments

def delete_teacher_instruments(db: Session, teacher_instrument_id: int):
    # Verificar si el nivel existe
    teachers_instruments = db.get(TeachersInstruments, teacher_instrument_id)
    if not teachers_instruments:
        return False  # Nivel no encontrado

    # Eliminar el nivel
    try:
        db.delete(teachers_instruments)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(f"Error al eliminar el nivel: {str(e)}")
        return False