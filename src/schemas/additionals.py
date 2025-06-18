from typing import Optional
from src.schemas.base import BasePydanticModel


class AdditionalRequest(BasePydanticModel):
    name: str
    description: Optional[str]

class Additional(AdditionalRequest):
    id: int
