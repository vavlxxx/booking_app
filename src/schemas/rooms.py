from pydantic import Field

from src.schemas.base import BasePydanticModel 


class Room(BasePydanticModel):
    title: str = Field(description="Название номера", example="Стандарт")
    description: str | None = Field(description="Описание номера", example="Номер в отеле в центре Москвы", default=None)
    quantity: int = Field(description="Количество номеров", example=10)
    price: float = Field(description="Цена", example=1000.00)
    discount: int | None = Field(default=0, le=100, ge=0, description="Скидка", example=10)


class FullRoomData(Room):
    id: int
    hotel_id: int = Field(description="ID отеля", example=1)
    discounted_price: float

class RoomDataWithEmptyRooms(FullRoomData):
    empty: int


class RoomOptional(BasePydanticModel):
    title: str | None = Field(default=None, description="Название номера", example="Стандарт")
    description: str | None = Field(description="Описание номера", example="Номер в отеле в центре Москвы", default=None)
    quantity: int | None = Field(description="Количество номеров", example=10, default=None)
    price: float | None = Field(description="Цена", example=1000.00, default=None)
    discount: int | None = Field(default=0, le=100, ge=0, description="Скидка", example=10)
