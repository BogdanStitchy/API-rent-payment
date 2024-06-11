from app.dao.base import BaseDAO
from app.rent_payment.model_rent_payment import RentPayment


class RentPaymentDAO(BaseDAO):
    model = RentPayment
