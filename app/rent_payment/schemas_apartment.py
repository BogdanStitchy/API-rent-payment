from pydantic import BaseModel
from datetime import date



class RentPaymentBase(BaseModel):
    id: int
    period: date
    apartment_id: int
    amount_due: float
