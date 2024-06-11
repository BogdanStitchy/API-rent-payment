from datetime import date, timedelta
from fastapi import APIRouter, status, Response, HTTPException
from celery.result import AsyncResult

from app.houses.schemas_house import HouseCreate, HouseRead
from app.houses.dao_house import HouseDAO
from app.tasks.tasks import calculate_rent_task

router = APIRouter(
    prefix="/rent",
    tags=["Квартплата"]
)


@router.post("/calculate_rent/{house_id}/{month}")
async def calculate_rent(house_id: int, selected_date: date):
    try:
        task = calculate_rent_task.apply_async(args=[house_id, selected_date])
        # task =  calculate_rent_task.delay(house_id, selected_date)
        return {"message": "Rent calculation started", "task_id": task.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred")


@router.get("/task_status/{task_id}")
def get_task_status(task_id: str):
    task = AsyncResult(task_id)
    return {"task_id": task.id, "status": task.status, "result": task.result}
