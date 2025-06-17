from datetime import datetime, timezone
from pydantic import Field, FutureDate, field_validator, model_validator, AwareDatetime  

from src.schemas.base import BasePydanticModel


class BookingRequest(BasePydanticModel):
    room_id: int = Field(description="ID номера", example=1, ge=1)
    date_from: FutureDate = Field(description="Дата заезда", example="2030-06-17")
    date_to: FutureDate = Field(description="Дата выезда", example="2030-06-20")

    @model_validator(mode="after")
    def validate_date(self) -> str:
        if self.date_from > self.date_to:
            raise ValueError("Date from must be less than date to")
        return self


class BookingWIthUser(BookingRequest):
    user_id: int


class BookingAdd(BookingWIthUser):
    price: float


class Booking(BookingAdd):
    id: int
