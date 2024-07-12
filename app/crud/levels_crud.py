from sqlalchemy import select
from sqlalchemy.orm import Session

from models import Level, Instrument

def get_level(db: Session, level_id: int):
    stmt = select(Level).where(Level.id == level_id)
    result = db.scalars(stmt).first()
    return result

# Listar todos los niveles
def get_levels(db: Session):
	stmt = select(Level)
	return db.scalars(stmt).all()

# Crear un nuevo nivel
def create_level(db: Session, instruments_id: int, level: str):
    # Verificar si ya existe un nivel con el mismo instrumento y nivel
    stmt = select(Level).where(
        (Level.instruments_id == instruments_id) & 
        (Level.level == level)
    )
    result = db.execute(stmt).scalars().first()
    if result:
        return None  # Nivel ya existente

    # Crear un nuevo nivel
    new_level = Level(
        instruments_id=instruments_id,
        level=level
    )
    db.add(new_level)
    db.commit()
    db.refresh(new_level)  # Refrescar la instancia para obtener los datos actualizados de la base de datos
    return new_level

def update_level(db: Session, level_id: int, **kwargs):
    # Verificar si el nivel existe
    level = db.get(Level, level_id)
    if not level:
        return None  # Nivel no encontrado

    # Actualizar los campos del nivel
    for key, value in kwargs.items():
        if hasattr(level, key):
            setattr(level, key, value)

    db.commit()
    db.refresh(level)  # Refrescar la instancia para obtener los datos actualizados de la base de datos
    return level

def delete_level(db: Session, level_id: int):
    # Verificar si el nivel existe
    level = db.get(Level, level_id)
    if not level:
        return False  # Nivel no encontrado

    # Eliminar el nivel
    try:
        db.delete(level)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(f"Error al eliminar el nivel: {str(e)}")
        return False