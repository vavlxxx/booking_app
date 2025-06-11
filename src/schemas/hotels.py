from pydantic import BaseModel, Field


class Hotel(BaseModel):
    title: str = Field(default=None, description="Заголовок")
    name: str = Field(default=None, description="Название отеля")


class HotelPATCH(BaseModel):
    title: str | None = Field(default=None, description="Заголовок")
    name: str | None = Field(default=None, description="Название отеля")
