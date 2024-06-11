from datetime import date
import asyncio

from app.tasks.celery import celery
from app.rent_payment.service_rent_payment import ServiceRentPayment


@celery.task
def calculate_rent_task(house_id: int, selected_date: date):
    asyncio.run(ServiceRentPayment.calculate_rent_for_house(house_id, selected_date))
