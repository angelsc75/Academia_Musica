from app.models import Pack, Instrument, PacksInstruments

from app.db import session

def create_pack(pack, discount_1, discount_2):
    new_pack = Pack(pack=pack, discount_1=discount_1, discount_2=discount_2)
    session.add(new_pack)
    session.commit()
    return new_pack

def get_pack(pack_id):
    pack = session.get(Pack, pack_id)
    return pack

def view_pack_details(pack_id):
    pack = session.get(Pack, pack_id)
    if not pack:
        return "Pack no encontrado."

    instruments = session.query(Instrument).join(PacksInstruments).filter(PacksInstruments.packs_id == pack_id).all()

    output = f"Detalles del Pack para el ID {pack.id}:\n"
    output += f"Pack: {pack.pack}\n"
    output += f"Descuento 1: {pack.discount_1}\n"
    output += f"Descuento 2: {pack.discount_2}\n"
    output += "Instrumentos incluidos:\n"

    if instruments:
        for instrument in instruments:
            output += f"- {instrument.name}\n"
    else:
        output += "No se encontraron instrumentos para este pack.\n"

    return output

def update_pack(pack_id, **kwargs):
    pack = session.get(Pack, pack_id)
    if pack:
        for key, value in kwargs.items():
            setattr(pack, key, value)
        session.commit()
        return pack
    return None

def delete_pack(pack_id):
    pack = session.get(Pack, pack_id)
    if pack:
        try:
            session.delete(pack)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"Error al eliminar el pack: {str(e)}")
            return False
    else:
        return False

def get_all_packs():
    packs = session.query(Pack).all()
    return packs