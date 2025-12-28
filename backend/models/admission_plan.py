from sqlalchemy import Column, Integer, BigInteger
from database import Base

class AdmissionPlan(Base):
    __tablename__ = "admission_plans_2026"

    id = Column(BigInteger, primary_key=True)
    institution_id = Column(Integer)
    specialty_id = Column(Integer)
    price = Column(Integer)
    plan_count = Column(Integer)
