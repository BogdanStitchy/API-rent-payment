from sqlalchemy import Column, Integer, Float, Date, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db import Base


class RentPayment(Base):
    __tablename__ = "rent_payment"
    id = Column(Integer, primary_key=True, index=True)
    period = Column(Date, nullable=False)
    apartment_id = Column(Integer, ForeignKey('apartments.id'), nullable=False)
    amount_due = Column(Float, nullable=False)

    apartment = relationship("Apartment", back_populates="rent")

    __table_args__ = (UniqueConstraint('period', 'apartment_id', name='_period_apartment_uc'),)

