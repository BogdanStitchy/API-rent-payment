from pydantic import BaseModel
from typing import List


class HouseBase(BaseModel):
    address: str


class HouseCreate(HouseBase):
    pass


class ApartmentRead(BaseModel):
    id_apartment: int
    number_apartment: int
    area_apartment: float


class HouseRead(HouseBase):
    id_house: int
    apartments: List[ApartmentRead]
