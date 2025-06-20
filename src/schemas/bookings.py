from pydantic import Field, FutureDate, model_validator  

from src.schemas.base import BasePydanticModel


class BookingRequest(BasePydanticModel):
    room_id: int = Field(description="ID номера", example=1, ge=1)
    date_from: FutureDate
    date_to: FutureDate

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
