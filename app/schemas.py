from pydantic import BaseModel, EmailStr
from decimal import Decimal
from typing import Optional
from datetime import date
from enum import Enum

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


class StudentBase(BaseModel):
    first_name: str
    last_name: str
    age: int
    phone: str
    mail: str
    family_id: Optional[bool] = None


class StudentCreate(StudentBase):
    pass


class Student(StudentBase):
    id: int

    class Config:
        orm_mode = True
        

class InscriptionBase(BaseModel):
    student_id: int
    level_id: int
    registration_date: date


class InscriptionCreate(InscriptionBase):
    pass


class Inscription(InscriptionBase):
    id: int

    class Config:
        orm_mode = True


class InscriptionDetail(BaseModel):
    inscription_id: int
    student_id: int
    student_name: str
    instrument_name: str
    level: str
    registration_date: str
    instrument_price: float

    class Config:
        orm_mode = True


class FeeReport(BaseModel):
    student_id: int
    first_name: str
    last_name: str
    total_fee: float
    inscription_count: int
    family_discount: str

    class Config:
        orm_mode = True

class LevelCreate(BaseModel):
    instruments_id: int
    level: str

class Level(LevelCreate):
	id: int

class LevelUpdate(BaseModel):
    instruments_id: Optional[int]
    level: Optional[str]

    class Config:
        orm_mode = True
        
class PackCreate(BaseModel):
    pack: str
    discount_1: float
    discount_2: float
class Pack(PackCreate):
    id: int
class PackUpdate(BaseModel):
    pack: Optional[str]
    discount_1: Optional[float]
    discount_2: Optional[float]

    class Config:
        orm_mode = True
        
class PacksInstrumentsCreate(BaseModel):
    
    pack_id: int
    instrument_id: int
class PacksInstruments(PacksInstrumentsCreate):
    id: int
class PacksInstrumentsUpdate(BaseModel):
    pack_id: Optional[int]
    instrument_id: Optional[int]
    

    class Config:
        orm_mode = True
        
class TeachersInstrumentsCreate(BaseModel):
    teacher_id: int
    instrument_id: int
    
class TeachersInstruments(TeachersInstrumentsCreate):
    id: int
class TeachersInstrumentsUpdate(BaseModel):
    teacher_id: Optional[int]
    instrument_id: Optional[int]
    
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

# Definimos los roles de usuario
class RoleEnum(str, Enum):
    admin = "Admin"
    gestor = "Gestor"

# Esquema base para el usuario
class UserBase(BaseModel):
    username: str
    email: EmailStr
    is_active: bool = True
    role: RoleEnum

# Esquema para crear un nuevo usuario
class UserCreate(UserBase):
    password: str

# Esquema para actualizar un usuario existente
class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None
    role: Optional[RoleEnum] = None

# Esquema para leer un usuario
class User(UserBase):
    id: int

    class Config:
        orm_mode: True