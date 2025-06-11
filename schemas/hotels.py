from pydantic import BaseModel, Field


class Hotel(BaseModel):
    title: str = Field(default=None, description="Заголовок")
    name: str = Field(default=None, description="Название отеля")


class HotelPATCH(BaseModel):
    title: str | None = Field(default=None, description="Заголовок")
    name: str | None = Field(default=None, description="Название отеля")


class HotelQueryParams(BaseModel):
    id_: int | None = Field(default=None, description="ID отеля (для фильтрации)")
    title: str | None = Field(default=None, description="Заголовок (для фильтрации)")
    page: int = Field(default=1, ge=1, description="Номер страницы")
    per_page: int = Field(
        default=5, ge=1, le=10, description="Количество отелей на странице"
    )
