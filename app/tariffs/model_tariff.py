from sqlalchemy import Column, Integer, String, Float
from app.db import Base


class Tariff(Base):
    __tablename__ = "tariffs"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    rate = Column(Float, nullable=False)
