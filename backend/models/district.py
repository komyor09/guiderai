from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from database import Base

class District(Base):
    __tablename__ = "districts"

    id = Column(Integer, primary_key=True)
    region_id = Column(Integer, ForeignKey("regions.id"))
    name = Column(String(100))
    type = Column(Enum("district", "city_of_region"))
