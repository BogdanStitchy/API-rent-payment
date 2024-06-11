from fastapi import APIRouter, status, Response, HTTPException

from app.houses.schemas_house import HouseCreate, HouseRead
from app.houses.dao_house import HouseDAO

router = APIRouter(
    prefix="/houses",
    tags=["Дома"]
)


@router.post("/add")
async def add_house(house: HouseCreate):
    adding_status = await HouseDAO.add(address=house.address)
    if "error" in adding_status:
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(status_code=status.HTTP_201_CREATED)


@router.get("/{house_id}")
async def get_one_house(house_id: int) -> HouseRead:
    db_house = await HouseDAO.find_by_id(house_id)
    if isinstance(db_house, dict):
        if "error" in db_house:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return db_house


@router.get("/")
async def get_houses():
    db_houses = await HouseDAO.get_all()
    if isinstance(db_houses, dict):
        if "error" in db_houses:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return db_houses
