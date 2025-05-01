# ==========================
# main.py (FastAPI backend)
# ==========================
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from db import Reed, SessionLocal
from sqlalchemy.orm import Session
import datetime

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ReedCreate(BaseModel):
    name: str
    notes: str = ""

class ReedUpdate(BaseModel):
    notes: str

@app.post("/reeds/")
def create_reed(reed: ReedCreate, db: Session = Depends(get_db)):
    db_reed = Reed(name=reed.name, notes=reed.notes)
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