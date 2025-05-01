# ==========================
# db.py
# ==========================
from sqlalchemy import Column, Integer, String, Date, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

DATABASE_URL = "sqlite:///./reeds.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Reed(Base):
    __tablename__ = "reeds"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    created_at = Column(Date, default=datetime.date.today)
    notes = Column(Text, default="")

Base.metadata.create_all(bind=engine)