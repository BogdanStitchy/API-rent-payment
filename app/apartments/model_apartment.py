from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.db import Base


class Apartment(Base):
    __tablename__ = "apartments"
    id = Column(Integer, primary_key=True, index=True)
    number = Column(Integer, index=True)
    area = Column(Float, nullable=False)
    house_id = Column(Integer, ForeignKey("houses.id"))

    house = relationship("House", back_populates="apartments")
    water_meters = relationship("WaterMeter", back_populates="apartment")
    rent = relationship("RentPayment", back_populates="apartment")

