# ==========================
# main.py (FastAPI backend)
# ==========================
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from db import Reed, SessionLocal
from sqlalchemy.orm import Session
import datetime
from fastapi import HTTPException

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ReedCreate(BaseModel):
    name: str
    instrument: str
    cane_type: str = ""
    shape: str = ""
    staple: str = ""
    gouge: str = ""
    reed_length: str = ""
    density: str = ""
    scrape: str = ""
    notes: str = ""
    quality: str = ""

class ReedUpdate(BaseModel):
    notes: str

@app.post("/reeds/")
def create_reed(reed: ReedCreate, db: Session = Depends(get_db)):
    db_reed = Reed(name=reed.name, notes=reed.notes, cane_type=reed.cane_type,
                   instrument = reed.instrument, shape = reed.shape, staple = reed.staple,
                   gouge = reed.gouge, scrape = reed.scrape, reed_length = reed.reed_length,
                   density = reed.density, quality = reed.quality)
    db.add(db_reed)
    db.commit()
    db.refresh(db_reed)
    return db_reed

@app.get("/reeds/")
def list_reeds(db: Session = Depends(get_db)):
    return db.query(Reed).all()

@app.post("/reeds/{reed_id}/add_note")
def add_note(reed_id: int, update: ReedUpdate, db: Session = Depends(get_db)):
    reed = db.query(Reed).filter(Reed.id == reed_id).first()
    if not reed:
        raise HTTPException(status_code=404, detail="Reed not found")
    reed.notes += f"\n{datetime.date.today()}: {update.notes}"
    db.commit()
    return reed

@app.delete("/reeds/{reed_id}/")
def delete_reed(reed_id: int, db: Session = Depends(get_db)):
    reed = db.query(Reed).filter(Reed.id == reed_id).first()
    if not reed:
        raise HTTPException(status_code=404, detail="Reed not found")
    db.delete(reed)
    db.commit()
    return {"message": "Reed deleted"}


class ReedEdit(BaseModel):
    instrument: str = ""
    cane_type: str = ""
    shape: str = ""
    staple: str = ""
    gouge: str = ""
    reed_length: str = ""  
    density: str = ""      
    scrape: str = ""
    notes: str = ""
    quality: str = ""      


@app.put("/reeds/{reed_id}/")
def update_reed(reed_id: int, reed_update: ReedEdit, db: Session = Depends(get_db)):
    reed = db.query(Reed).filter(Reed.id == reed_id).first()
    if not reed:
        raise HTTPException(status_code=404, detail="Reed not found")

    for field, value in reed_update.dict().items():
        setattr(reed, field, value)

    db.commit()
    db.refresh(reed)
    return reed
