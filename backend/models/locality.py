from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from database import Base

class Locality(Base):
    __tablename__ = "localities"

    id = Column(Integer, primary_key=True)
    district_id = Column(Integer, ForeignKey("districts.id"))
    name = Column(String(100))
    type = Column(Enum("city", "township", "jamoat"))
