from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db import SessionLocal
from app import crud
from app import schemas

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@app.get("/levels/{level_id}", response_model=schemas.Level)
def read_level(level_id: int, db: Session = Depends(get_db)):
    db_level = crud.get_level(db, level_id=level_id)
    if db_level is None:
        raise HTTPException(status_code=404, detail="Nivel no encontrado")
    return db_level

@app.get("/levels/", response_model=List[schemas.Level])
def read_levels(db: Session = Depends(get_db)):
    return crud.get_levels(db)

@app.post("/levels/", response_model=schemas.Level)
def create_level(level: schemas.LevelCreate, db: Session = Depends(get_db)):
    db_level = crud.create_level(db, instruments_id=level.instruments_id, level=level.level)
    if db_level is None:
        raise HTTPException(status_code=400, detail="El nivel ya existe")
    return db_level

@app.put("/levels/{level_id}", response_model=schemas.Level)
def update_level(level_id: int, level_update: schemas.LevelUpdate, db: Session = Depends(get_db)):
    db_level = crud.update_level(db, level_id=level_id, **level_update.dict())
    if db_level is None:
        raise HTTPException(status_code=404, detail="Nivel no encontrado")
    return db_level

@app.delete("/levels/{level_id}", response_model=bool)
def delete_level(level_id: int, db: Session = Depends(get_db)):
    success = crud.delete_level(db, level_id=level_id)
    if not success:
        raise HTTPException(status_code=404, detail="Nivel no encontrado")
    return success

@app.get("/packs/{pack_id}", response_model=schemas.Pack)
def read_pack(pack_id: int, db: Session = Depends(get_db)):
    db_pack = crud.get_pack(db, pack_id=pack_id)
    if db_pack is None:
        raise HTTPException(status_code=404, detail="Pack no encontrado")
    return db_pack

@app.get("/packs/", response_model=List[schemas.Pack])
def read_packs(db: Session = Depends(get_db)):
    return crud.get_packs(db)

@app.post("/packs/", response_model=schemas.Pack)
def create_pack(pack: schemas.PackCreate, db: Session = Depends(get_db)):
    db_pack = crud.create_pack(db, pack=pack.pack, discount_1=pack.discount_1, discount_2=pack.discount_2)
    if db_pack is None:
        raise HTTPException(status_code=400, detail="El pack ya existe")
    return db_pack

@app.put("/packs/{pack_id}", response_model=schemas.Pack)
def update_pack(pack_id: int, pack_update: schemas.PackUpdate, db: Session = Depends(get_db)):
    db_pack = crud.update_pack(db, pack_id=pack_id, **pack_update.dict(exclude_unset=True))
    if db_pack is None:
        raise HTTPException(status_code=404, detail="Pack no encontrado")
    return db_pack

@app.delete("/packs/{pack_id}", response_model=bool)
def delete_pack(pack_id: int, db: Session = Depends(get_db)):
    success = crud.delete_pack(db, pack_id=pack_id)
    if not success:
        raise HTTPException(status_code=404, detail="Pack no encontrado")
    return success