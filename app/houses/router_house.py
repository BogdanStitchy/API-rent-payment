from fastapi import APIRouter, status, Response

from app.houses.schemas_house import HouseCreate, HouseRead
from app.houses.dao_house import HouseDAO

router = APIRouter(
    prefix="/houses",
    tags=["Дома"]
)


@router.post("/houses")
async def create_house(house: HouseCreate):
    adding_status = await HouseDAO.add(address=house.address)
    if "error" in adding_status:
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(status_code=status.HTTP_201_CREATED)


@router.get("/{house_id}")
async def read_house(house_id: int) -> list[HouseRead]:
    db_house_id = await HouseDAO.find_by_id(house_id)

    if isinstance(db_house_id, str):
        if "error" in db_house_id:
            return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return db_house_id
