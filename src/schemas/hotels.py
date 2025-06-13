from pydantic import BaseModel, Field


class Hotel(BaseModel):
    title: str = Field(description="Заголовок", example="Hotel Deluxe")
    location: str = Field(description="Адрес", example="г. Москва, ул. Пушкинская, д. 5")


class HotelNullable(BaseModel):
    title: str | None = Field(default=None, description="Заголовок", example="Hotel Deluxe")
    location: str | None = Field(default=None, description="Адрес", example="г. Москва, ул. Пушкинская, д. 5")
