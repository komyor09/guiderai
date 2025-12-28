from sqlalchemy import Column, Integer, String
from database import Base

class Specialty(Base):
    __tablename__ = "specialties"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
