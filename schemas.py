from pydantic import BaseModel
from typing import List, Optional
from datetime import date



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

