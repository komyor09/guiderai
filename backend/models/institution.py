from sqlalchemy import Column, Integer, String
from database import Base

class Institution(Base):
    __tablename__ = "institutions"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    region = Column(String(100))
