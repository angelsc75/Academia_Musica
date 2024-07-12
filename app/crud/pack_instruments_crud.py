from sqlalchemy import select
from sqlalchemy.orm import Session

from models import PacksInstruments
# Listar un paquete de instrumentos
def get_pack_instruments(db: Session, packs_instruments_id: int):
    stmt = select(PacksInstruments).where(PacksInstruments.id == packs_instruments_id)
    result = db.scalars(stmt).first()
    return result

# Listar todos los paquetes
def get_packs_instruments(db: Session):
	stmt = select(PacksInstruments)
	return db.scalars(stmt).all()

# Crear un nuevo paquete de instrumentos
def create_packs_instruments(db: Session, packs_instrument_id: int, instrument_id: int, packs_id: int):
    # Verificar si ya existe un nivel con el mismo instrumento y nivel
    stmt = select(PacksInstruments).where(
        (PacksInstruments.instrument_id == instrument_id) and 
        (PacksInstruments.packs_id == packs_id)
    )
    result = db.execute(stmt).scalars().first()
    if result is not None:
        return None  # Nivel ya existente

    # Crear un nuevo nivel
    new_pack_instruments = PacksInstruments(
        packs_instrument_id=packs_instrument_id,
        instrument_id=instrument_id,
        packs_id=packs_id
    )
    db.add(new_pack_instruments)
    db.commit()
    db.refresh(new_pack_instruments)  # Refrescar la instancia para obtener los datos actualizados de la base de datos
    return new_pack_instruments

def update_packs_instruments(db: Session, packs_instruments_id: int, **kwargs):
    # Verificar si el nivel existe
    packs_instuments = db.get(PacksInstruments, packs_instruments_id)
    if not packs_instuments:
        return None  # Nivel no encontrado

    # Actualizar los campos del nivel
    for key, value in kwargs.items():
        if hasattr(packs_instuments, key):
            setattr(packs_instuments, key, value)

    db.commit()
    db.refresh(packs_instuments)  # Refrescar la instancia para obtener los datos actualizados de la base de datos
    return packs_instuments

def delete_packs_instruments(db: Session, packs_instruments_id: int):
    # Verificar si el nivel existe
    packs_instruments = db.get(PacksInstruments, packs_instruments_id)
    if not packs_instruments:
        return False  # Nivel no encontrado

    # Eliminar el nivel
    try:
        db.delete(packs_instruments)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(f"Error al eliminar el pack de instrumentos: {str(e)}")
        return False