from app.dao.base import BaseDAO
from app.tariffs.model_tariff import Tariff


class TariffDAO(BaseDAO):
    model = Tariff
