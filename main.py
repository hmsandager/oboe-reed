# ==========================
# main.py (FastAPI backend)
# ==========================
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from db import Reed, User, SessionLocal
from sqlalchemy.orm import Session
import datetime
from fastapi import HTTPException
import bcrypt

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class LoginData(BaseModel):
    username: str
    password: str

@app.post("/login/")
def login(data: LoginData, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()
    if not user or not bcrypt.checkpw(data.password.encode('utf-8'), user.hashed_password.encode('utf-8')):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"user_id": user.id}


class ReedCreate(BaseModel):
    user_id: str  
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
    db_reed = Reed(user_id=reed.user_id, name=reed.name, notes=reed.notes, cane_type=reed.cane_type,
                   instrument = reed.instrument, shape = reed.shape, staple = reed.staple,
                   gouge = reed.gouge, scrape = reed.scrape, reed_length = reed.reed_length,
                   density = reed.density, quality = reed.quality)
    db.add(db_reed)
    db.commit()
    db.refresh(db_reed)
    return db_reed

@app.get("/reeds/")
def list_reeds(user_id: str, db: Session = Depends(get_db)):
    return db.query(Reed).filter(Reed.user_id == user_id).all()

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
    user_id: str = ""
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
