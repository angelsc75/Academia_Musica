from pydantic import BaseModel
from decimal import Decimal
from typing import Optional

class CreateTeacher(BaseModel):
	first_name: str
	last_name: str
	phone: str
	mail: str

class Teacher(CreateTeacher):
	id: int
     
class UpdateTeacher(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    mail: Optional[str] = None


#######Instruments (borrar)
class InstrumentBase(BaseModel):
    name: str
    price: Decimal

class CreateInstrument(InstrumentBase):
    pass # Hereda todos los campos de InstrumentBase sin añadir campos adicionales
class UpdateInstrument(BaseModel):
    name: Optional[str] = None
    price: Optional[Decimal] = None

class Instrument(InstrumentBase):
    id: int

    class Config:
        orm_mode = True # Permite que Pydantic lea los datos incluso si no son dict
        # Esto es útil cuando los datos provienen de un ORM