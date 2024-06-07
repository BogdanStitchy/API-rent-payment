from pydantic import BaseModel
from typing import List
from app.apartments.schemas_apartment import ApartmentRead


class HouseBase(BaseModel):
    address: str


class HouseCreate(HouseBase):
    pass


class HouseRead(HouseBase):
    id_house: int
    id_apartment: int
    number_apartment: int
    area_apartment: float
