from datetime import date

from pydantic import Field, FutureDate 

from src.schemas.base import BasePydanticModel


class BookingRequest(BasePydanticModel):
    room_id: int = Field(description="ID номера", ge=1)
    date_from: FutureDate | date
    date_to: FutureDate | date

    # @model_validator(mode="after")
    # def validate_date(self) -> str:
    #     if self.date_from > self.date_to:
    #         raise ValueError("Дата въезда не может быть позднее даты выезда")
    #     return self


class BookingAdd(BookingRequest):
    user_id: int
    price: float


class Booking(BookingAdd):
    id: int
