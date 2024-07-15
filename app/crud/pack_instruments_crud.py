from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
import logging

from models import PacksInstruments, Pack, Instrument


# Obtener el logger configurado
logger = logging.getLogger("music_app")

# Listar un pack de instrumentos
def get_pack_instruments(db: Session, packs_instruments_id: int):
    try:
        stmt = select(PacksInstruments).where(PacksInstruments.id == packs_instruments_id)
        result = db.scalars(stmt).first()
        logger.info("Pack de instrumentos no encontrado")
        if not result:
            raise HTTPException(status_code=404, detail="Pack de instrumentos no encontrado")
        return result
    except SQLAlchemyError as e:
        logging.error(f"Error de base de datos al obtener pack de instrumentos: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al obtener pack de instrumentos")
    except Exception as e:
        logging.error(f"Error inesperado al obtener pack de instrumentos: {str(e)}")
        raise HTTPException(status_code=500, detail="Error inesperado al obtener pack de instrumentos")

# Listar todos los packs de instrumentos
def get_packs_instruments(db: Session):
    try:
        stmt = select(PacksInstruments)
        result = db.scalars(stmt).all()
        logger.info("Todos packs de instrumentos recuperados con éxito")        
        return result
    except SQLAlchemyError as e:
        logging.error(f"Error de base de datos al obtener packs de instrumentos: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al obtener packs de instrumentos")
    except Exception as e:
        logging.error(f"Error inesperado al obtener packs de instrumentos: {str(e)}")
        raise HTTPException(status_code=500, detail="Error inesperado al obtener packs de instrumentos")

# Crear un nuevo paquete de instrumentos
def create_packs_instruments(db: Session, instrument_id: int, packs_id: int):
    try:
        # Verificar si ya existe la combinación de instrumento y paquete
        stmt = select(PacksInstruments).where(
            (PacksInstruments.instrument_id == instrument_id) & 
            (PacksInstruments.packs_id == packs_id)
        )
        result = db.execute(stmt).scalars().first()
        if result is not None:
            logger.info("Combinación de instrumento y paquete ya existe")           
            raise HTTPException(status_code=400, detail="La combinación de instrumento y paquete ya existe")

        # Verificar si el instrumento existe
        instrument = db.get(Instrument, instrument_id)
        if not instrument:
            logger.info("Instrumento no encontrado")            
            raise HTTPException(status_code=404, detail="Instrumento no encontrado")

        # Verificar si el paquete existe
        pack = db.get(Pack, packs_id)
        if not pack:
            logger.info("Paquete no encontrado")
            raise HTTPException(status_code=404, detail="Paquete no encontrado")

        # Crear una nueva combinación de instrumento y paquete
        new_pack_instruments = PacksInstruments(
            instrument_id=instrument_id,
            packs_id=packs_id
        )
        db.add(new_pack_instruments)
        db.commit()
        db.refresh(new_pack_instruments)  # Refrescar la instancia para obtener los datos actualizados de la base de datos
        logger.info("Combinación de instrumento y paquete creada con éxito")
        return new_pack_instruments
    except SQLAlchemyError as e:
        db.rollback()
        logging.error(f"Error de base de datos al crear la combinación de instrumento y paquete: {str(e)}")
        raise HTTPException(status_code=500, detail="Error de base de datos")
    except HTTPException as e:
        logger.error(f"Error de base de datos al crear combinación de instrumento y paquete: {str(e)}")
        raise HTTPException(status_code=500, detail="Error de base de datos")    
    except Exception as e:
        db.rollback()
        logging.error(f"Error inesperado al crear la combinación de instrumento y paquete: {str(e)}")
        raise HTTPException(status_code=500, detail="Error inesperado")

def update_packs_instruments(db: Session, packs_instruments_id: int, **kwargs):
    try:
        # Verificar si la combinación de paquete e instrumento existe
        packs_instruments = db.get(PacksInstruments, packs_instruments_id)
        if not packs_instruments:
            logger.info("Combinación de paquete e instrumento no encontrado")            
            raise HTTPException(status_code=404, detail="La combinación de paquete e instrumento no encontrada")

        # Verificar si el instrumento existe (si está en kwargs)
        if 'instrument_id' in kwargs:
            instrument = db.get(Instrument, kwargs['instrument_id'])
            if not instrument:
                logger.info("Instrumento no encontrado")            
                raise HTTPException(status_code=404, detail="Instrumento no encontrado")

        # Verificar si el paquete existe (si está en kwargs)
        if 'packs_id' in kwargs:
            pack = db.get(Pack, kwargs['packs_id'])
            if not pack:
                logger.info("Paquete no encontrado")            
                raise HTTPException(status_code=404, detail="Paquete no encontrado")

        # Actualizar los campos de la combinación de paquete e instrumento
        for key, value in kwargs.items():
            if hasattr(packs_instruments, key):
                setattr(packs_instruments, key, value)

        db.commit()
        db.refresh(packs_instruments)  # Refrescar la instancia para obtener los datos actualizados de la base de datos
        logger.info("Combinación pack e insturmento actualizado con éxito")
        return packs_instruments

    except SQLAlchemyError as e:
        db.rollback()
        logging.error(f"Error de base de datos al actualizar la combinación de paquete e instrumento: {str(e)}")
        raise HTTPException(status_code=500, detail="Error de base de datos")
    except HTTPException as e:
        logger.error(f"Error de base de datos al crear combinación de instrumento y paquete: {str(e)}")
        raise HTTPException(status_code=500, detail="Error de base de datos")    
    except Exception as e:
        db.rollback()
        logging.error(f"Error inesperado al actualizar la combinación de paquete e instrumento: {str(e)}")
        raise HTTPException(status_code=500, detail="Error inesperado")

def delete_packs_instruments(db: Session, packs_instruments_id: int) -> bool:
    try:
        # Verificar si el pack de instrumentos existe
        packs_instruments = db.get(PacksInstruments, packs_instruments_id)
        if not packs_instruments:
            logger.info("Combinación de paquete e instrumento no encontrado")            
            raise HTTPException(status_code=404, detail="Pack de instrumentos no encontrado")

        # Eliminar el pack de instrumentos
        db.delete(packs_instruments)
        db.commit()
        logger.info("Combinación pack e insturmento actualizado con éxito")        
        return True
    except HTTPException as e:
        logger.error(f"Error de base de datos al crear combinación de instrumento y paquete: {str(e)}")
        raise HTTPException(status_code=500, detail="Error de base de datos")    
    except SQLAlchemyError as e:
        db.rollback()
        logging.error(f"Error de base de datos al eliminar el pack de instrumentos: {str(e)}")
        raise HTTPException(status_code=500, detail="Error de base de datos")
    except Exception as e:
        db.rollback()
        logging.error(f"Error inesperado al eliminar el pack de instrumentos: {str(e)}")
        raise HTTPException(status_code=500, detail="Error inesperado")