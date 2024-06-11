from datetime import date

from sqlalchemy import and_, select, func, extract, or_
from sqlalchemy.orm import selectinload, with_loader_criteria
from sqlalchemy.exc import SQLAlchemyError

from app.db import async_session_maker
from app.logger import logger
from app.dao.base import BaseDAO
from app.houses.model_house import House
from app.apartments.model_apartment import Apartment
from app.water_meters.model_water_meter import WaterMeter, WaterReading


class HouseDAO(BaseDAO):
    model = House

    @classmethod
    async def find_by_id(cls, house_id: int):
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
                       ).where(House.id == house_id).group_by(House.id, House.address)
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
                "model_id": house_id
            }
            logger.error(msg, extra=extra, exc_info=True)
            return {"error": error.__str__()}

    @classmethod
    async def get_object_house_model(cls, house_id: int, selected_date: date, previous_date: date):
        try:
            async with async_session_maker() as session:
                query = (
                    select(House)
                        .options(
                        selectinload(House.apartments)
                            .selectinload(Apartment.water_meters)
                            .selectinload(WaterMeter.readings),
                        with_loader_criteria(WaterReading,
                                             # будет получено только две записи с каждого счетчика: выбранный месяц и предыдущий месяц
                                             or_(
                                                 and_(
                                                     extract('year', WaterReading.date) == selected_date.year,
                                                     extract('month', WaterReading.date) == selected_date.month,
                                                 ),
                                                 and_(
                                                     extract('year', WaterReading.date) == previous_date.year,
                                                     extract('month', WaterReading.date) == previous_date.month,
                                                 ),
                                             )
                                             )
                    )
                        .where(House.id == house_id)
                )

                result = await session.execute(query)
                result = result.scalars().first()
                return result
        except (SQLAlchemyError, Exception) as error:
            if isinstance(error, SQLAlchemyError):
                msg = "Database Exc"
            if isinstance(error, Exception):
                msg = "Unknown Exc"
            msg += ": Cannot get object house"
            extra = {
                "model": cls.model,
                "model_id": house_id
            }
            logger.error(msg, extra=extra, exc_info=True)
            return {"error": error.__str__()}
