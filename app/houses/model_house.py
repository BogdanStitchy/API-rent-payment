from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db import Base


class House(Base):
    __tablename__ = "houses"
    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, index=True, unique=True)
    apartments = relationship("Apartment", back_populates="house")
