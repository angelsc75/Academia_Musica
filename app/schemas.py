from pydantic import BaseModel
from typing import Optional # Para actualizar sólo los campos necesarios

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


