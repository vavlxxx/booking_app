from src.models.hotels import HotelsOrm
from src.schemas.hotels import Hotel
from src.repos.mappers.base import DataMapper


class HotelsMapper(DataMapper):
    db_model = HotelsOrm
    schema = Hotel
    