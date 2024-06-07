from sqlalchemy import delete, insert, select, and_, func
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
                query = select(
                    House.id.label("id_house"),
                    House.address,
                    func.json_agg(
                        func.json_build_object(
                            'id_apartment', Apartment.id,
                            'number_apartment', Apartment.number,
                            'area_apartment', Apartment.area
                        )
                    ).label('apartments')
                ).join(Apartment, House.id == Apartment.house_id
                       ).where(House.id == model_id).group_by(House.id, House.address)
                result = await session.execute(query)
                return result.mappings().one()
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
