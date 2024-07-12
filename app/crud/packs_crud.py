from sqlalchemy import select
from sqlalchemy.orm import Session

from models import Pack

def get_pack(db: Session, pack_id: int):
    stmt = select(Pack).where(Pack.id == pack_id)
    result = db.scalars(stmt).first()
    return result

# Listar todos los packs
def get_packs(db: Session):
	stmt = select(Pack)
	return db.scalars(stmt).all()

# Crear un nuevo pack
def create_pack(db: Session, pack: str, discount_1: float, discount_2: float):
    stmt = select(Pack).where(Pack.pack == pack)
    result = db.execute(stmt).scalars().first()
    if result is not None:
        return None  # Nivel ya existente

    # Crear un nuevo nivel
    new_pack = Pack(pack=pack, discount_1=discount_1, discount_2=discount_2)
    db.add(new_pack)
    db.commit()
    db.refresh(new_pack)
    return new_pack

def update_pack(db: Session, pack_id: int, **kwargs):
    pack = db.get(Pack, pack_id)
    if not pack:
        return None

    for key, value in kwargs.items():
        if hasattr(pack, key):
            setattr(pack, key, value)

    db.commit()
    db.refresh(pack)
    return pack

def delete_pack(db: Session, pack_id: int):
    pack = db.get(Pack, pack_id)
    if not pack:
        return False

    try:
        db.delete(pack)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(f"Error al eliminar el pack: {str(e)}")
        return False