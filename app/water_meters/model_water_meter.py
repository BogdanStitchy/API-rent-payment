from sqlalchemy import Column, Integer, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from app.db import Base


class WaterMeter(Base):
    __tablename__ = "water_meters"
    id = Column(Integer, primary_key=True, index=True)
    apartment_id = Column(Integer, ForeignKey("apartments.id"))

    readings = relationship("WaterReading", back_populates="water_meter")


class WaterReading(Base):
    __tablename__ = "water_readings"
    id = Column(Integer, primary_key=True, index=True)
    meter_id = Column(Integer, ForeignKey("water_meters.id"))
    reading = Column(Float, nullable=False)
    date = Column(DateTime, nullable=False)

    water_meter = relationship("WaterMeter", back_populates="readings")
