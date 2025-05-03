# ==========================
# db.py
# ==========================
from sqlalchemy import Column, Integer, String, Date, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime
import os

DATABASE_URL = "postgresql://postgres:ohjGiDHIpuveYQmwfkSORYPfDDezYajw@postgres.railway.internal:5432/railway"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Reed(Base):
    __tablename__ = "reeds"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    created_at = Column(Date, default=datetime.date.today)

    cane_type = Column(String, default="")  # <-- NEW FIELD
    instrument = Column(String)
    shape = Column(String)
    staple = Column(String)
    gouge = Column(String)
    scrape = Column(String)
    notes = Column(String)
    density = Column(String)
    reed_length = Column(String)
    quality = Column(String)

Base.metadata.create_all(bind=engine)