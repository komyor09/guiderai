from sqlalchemy import Column, Integer, String, Enum
from database import Base

class Region(Base):
    __tablename__ = "regions"

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    type = Column(Enum("oblast", "rrp", "city"))
