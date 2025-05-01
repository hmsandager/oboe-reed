from db import SessionLocal, Reed

db = SessionLocal()
reeds = db.query(Reed).all()
print(reeds)
