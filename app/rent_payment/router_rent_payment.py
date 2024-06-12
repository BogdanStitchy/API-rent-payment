from datetime import date
from fastapi import APIRouter, HTTPException
from typing import List

from app.rent_payment.dao_rent_payment import RentPaymentDAO
from app.rent_payment.schemas_apartment import RentPaymentBase
from app.tasks.tasks import calculate_rent_task

router = APIRouter(
    prefix="/rent",
    tags=["Квартплата"]
)


@router.post("/calculate_rent/{house_id}/{month}")
async def calculate_rent(house_id: int, selected_date: date):
    try:
        task = calculate_rent_task.apply_async(args=[house_id, selected_date])
        return {"message": "Rent calculation started", "task_id": task.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred")


@router.get("/apart/{apart_id}")
async def get_rents_for_one_apartment(apartment_id: int) -> List[RentPaymentBase]:
    db_rent = await RentPaymentDAO.get_all(apartment_id=apartment_id)
    return db_rent


@router.get("/{month}")
async def get_rents_for_selected_month(month: date) -> List[RentPaymentBase]:
    month = month.replace(day=1)

    db_rent = await RentPaymentDAO.get_all(period=month)
    return db_rent
