from src.models.additionals import AdditionalsOrm
from src.schemas.additionals import Additional
from src.repos.base import BaseRepository


class AdditionalsRepository(BaseRepository):
    model = AdditionalsOrm
    schema = Additional
    not_found_message = "Дополнительное удобство не найдено"
    