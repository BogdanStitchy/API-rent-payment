from sqlalchemy import delete, insert, select, and_
from sqlalchemy.exc import SQLAlchemyError

from app.db import async_session_maker
from app.logger import logger
from app.dao.base import BaseDAO
from app.houses.model_house import House
from app.apartments.model_apartment import Apartment


class HouseDAO(BaseDAO):
    model = House

    @classmethod
    async def find_by_id(cls, model_id: int):
        try:
            async with async_session_maker() as session:
                query = select(House.id.label("id_house"),
                               House.address,
                               Apartment.id.label("id_apartment"),
                               Apartment.number.label("number_apartment"),
                               Apartment.area.label("area_apartment")
                               ).where(and_(
                               House.id == Apartment.house_id,
                               House.id == model_id))
                result = await session.execute(query)
                return result.mappings().all()
        except (SQLAlchemyError, Exception) as error:
            if isinstance(error, SQLAlchemyError):
                msg = "Database Exc"
            if isinstance(error, Exception):
                msg = "Unknown Exc"
            msg += ": Cannot find by id"
            extra = {
                "model": cls.model,
                "model_id": model_id
            }
            logger.error(msg, extra=extra, exc_info=True)
            return {"error": error.__str__()}
