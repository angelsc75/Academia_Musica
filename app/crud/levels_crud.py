from models import Level, Instrument
from app.db import session

# CRUD PARA NIVELES
def create_level(instruments_id, level):
    new_level = Level(instruments_id=instruments_id, level=level)
    session.add(new_level)
    session.commit()
    return new_level

def get_level(level_id):
    level = session.get(Level, level_id)
    return level

def view_level_details(level_id):
    level = session.get(Level, level_id)
    if not level:
        return "Nivel no encontrado."

    instrument = session.get(Instrument, level.instruments_id)

    output = f"Detalles del Nivel para el ID {level.id}:\n"
    output += f"Instrumento: {instrument.name}\n"
    output += f"Nivel: {level.level}\n"

    return output

def get_all_levels():
    levels = session.query(Level).all()
    return levels

def update_level(level_id, **kwargs):
    level = session.get(Level, level_id)
    if level:
        for key, value in kwargs.items():
            setattr(level, key, value)
        session.commit()
        return level
    return None

def delete_level(level_id):
    level = session.get(Level, level_id)
    if level:
        try:
            session.delete(level)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"Error al eliminar el nivel: {str(e)}")
            return False
    else:
        return False