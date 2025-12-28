from sqlalchemy import Column, Integer, BigInteger
from database import Base

class AdmissionPlanLanguage(Base):
    __tablename__ = "admission_plan_languages"

    admission_plan_id = Column(BigInteger, primary_key=True)
    language_id = Column(Integer, primary_key=True)
