from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
import logging
from typing import Optional, List
from models import Pack

def get_pack(db: Session, pack_id: int) -> Optional[Pack]:
    try:
        stmt = select(Pack).where(Pack.id == pack_id)
        result = db.scalars(stmt).first()
        if result is None:
            logging.info(f"Pack con ID {pack_id} no encontrado")
            raise HTTPException(status_code=404, detail="Pack no encontrado")
        logging.info(f"Pack con ID {pack_id} recuperado con éxito")
        return result
    except SQLAlchemyError as e:
        logging.error(f"Error de base de datos al obtener el pack con ID {pack_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        logging.error(f"Error inesperado al obtener el pack con ID {pack_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

# Listar todos los packs
def get_packs(db: Session) -> List[Pack]:
    try:
        stmt = select(Pack)
        logging.info("Todos los packs recuperados con éxito")
        return db.scalars(stmt).all()
    except SQLAlchemyError as e:
        logging.error(f"Error de base de datos al obtener los packs: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        logging.error(f"Error inesperado al obtener los packs: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

# Crear un nuevo pack
def create_pack(db: Session, pack: str, discount_1: float, discount_2: float) -> Optional[Pack]:
    stmt = select(Pack).where(Pack.pack == pack)
    result = db.execute(stmt).scalars().first()
    if result is not None:
        logging.info(f"Pack ya existente: {pack}")
        raise HTTPException(status_code=400, detail="Pack ya existente")

    new_pack = Pack(pack=pack, discount_1=discount_1, discount_2=discount_2)
    db.add(new_pack)

    try:
        db.commit()
        db.refresh(new_pack)
        logging.info(f"Pack creado con éxito: {new_pack}")
        return new_pack
    except SQLAlchemyError as e:
        db.rollback()
        logging.error(f"Error de base de datos al crear el pack: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        db.rollback()
        logging.error(f"Error inesperado al crear el pack: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

def update_pack(db: Session, pack_id: int, **kwargs) -> Optional[Pack]:
    try:
        pack = db.get(Pack, pack_id)
        if not pack:
            logging.info(f"Pack con ID {pack_id} no encontrado para actualización")
            raise HTTPException(status_code=404, detail="Pack no encontrado")

        for key, value in kwargs.items():
            if hasattr(pack, key):
                setattr(pack, key, value)

        db.commit()
        db.refresh(pack)
        logging.info(f"Pack con ID {pack_id} actualizado con éxito")
        return pack
    except SQLAlchemyError as e:
        db.rollback()
        logging.error(f"Error de base de datos al actualizar el pack con ID {pack_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        db.rollback()
        logging.error(f"Error inesperado al actualizar el pack con ID {pack_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

def delete_pack(db: Session, pack_id: int) -> bool:
    try:
        pack = db.get(Pack, pack_id)
        if not pack:
            logging.info(f"Pack con ID {pack_id} no encontrado para eliminación")
            raise HTTPException(status_code=404, detail="Pack no encontrado")

        db.delete(pack)
        db.commit()
        logging.info(f"Pack con ID {pack_id} eliminado con éxito")
        return True
    except SQLAlchemyError as e:
        db.rollback()
        logging.error(f"Error de base de datos al eliminar el pack con ID {pack_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        db.rollback()
        logging.error(f"Error inesperado al eliminar el pack con ID {pack_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")