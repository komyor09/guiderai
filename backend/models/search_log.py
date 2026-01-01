from sqlalchemy import Column, Integer, BigInteger, String, Boolean, DateTime
from sqlalchemy.sql import func
from database import Base


class SearchLog(Base):
    __tablename__ = "search_logs"

    id = Column(BigInteger, primary_key=True)
    language = Column(String(50))
    specialty = Column(String(255))
    budget = Column(Boolean)

    region_id = Column(Integer)
    district_id = Column(Integer)
    locality_id = Column(Integer)

    sort = Column(String(50))
    order = Column(String(10))

    created_at = Column(DateTime, server_default=func.now())
