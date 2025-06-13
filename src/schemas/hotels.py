from pydantic import BaseModel, Field


class Hotel(BaseModel):
    title: str = Field(default=None, description="Заголовок")
    location: str = Field(default=None, description="Название отеля")


class HotelPATCH(BaseModel):
    title: str | None = Field(default=None, description="Заголовок")
    location: str | None = Field(default=None, description="Название отеля")
