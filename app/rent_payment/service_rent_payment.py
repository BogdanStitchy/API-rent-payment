from datetime import date

from dateutil.relativedelta import relativedelta

from app.houses.dao_house import HouseDAO
from app.rent_payment.dao_rent_payment import RentPaymentDAO
from app.houses.model_house import House
from app.tariffs.dao_tariff import TariffDAO


class ServiceRentPayment:
    @classmethod
    async def calculate_rent_for_house(cls, house_id: int, selected_date: date):
        previous_date = selected_date - relativedelta(months=1)  # предыдущий месяц
        house = await HouseDAO.get_object_house_model(house_id, selected_date, previous_date)

        await cls.__calculate_all_rent_apartments_in_house(house, selected_date)

    @classmethod
    async def __calculate_all_rent_apartments_in_house(cls, house: House, selected_date: date):
        for apartment in house.apartments:
            total_readings_all_meters_in_apartment = 0
            for water_meter in apartment.water_meters:
                one_of_records = -1  # В условии не сказано про возможное отсутствие одной из записей (прошлый или текущий месяц), поэтому принято условие, что обе записи имеются в базе
                total_meter_reading = 0
                for reading in water_meter.readings:
                    if one_of_records == -1:  # рассматривается первая из двух записей
                        one_of_records = reading.reading
                    else:  # рассматривается вторая из двух записей
                        total_meter_reading = abs(reading.reading - one_of_records)
                        total_readings_all_meters_in_apartment += total_meter_reading

            await cls.__calculate_rent_for_apartment(id_apartment=apartment.id,
                                                     # для одинакового числа месяца во всех записях квартплаты
                                                     period=selected_date.replace(day=1),
                                                     apartment_area=apartment.area,
                                                     water_meter_readings=total_readings_all_meters_in_apartment)

    @classmethod
    async def __calculate_rent_for_apartment(cls, id_apartment: int, period: date, apartment_area: float,
                                             water_meter_readings: float):
        price_tariff_water = await TariffDAO.find_one_or_none(id=1)
        price_tariff_area = await TariffDAO.find_one_or_none(id=2)
        price_tariff_water = price_tariff_water.rate
        price_tariff_area = price_tariff_area.rate

        final_rent = apartment_area * price_tariff_area + water_meter_readings * price_tariff_water

        await RentPaymentDAO.add(apartment_id=id_apartment,
                                 period=period,
                                 amount_due=final_rent
                                 )
