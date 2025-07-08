from typing import Type

from sqlalchemy import Row, RowMapping

from src.schemas.base import BasePydanticModel
from src.db import Base

# SchemaType = TypeVar("SchemaType", bound=BasePydanticModel)
# DBModelType = TypeVar("DBModelType", bound=Base)

class DataMapper:
    db_model: Type[Base]
    schema: Type[BasePydanticModel]

    @classmethod
    def map_to_domain_entity(cls, db_model: Base | dict | Row | RowMapping) -> BasePydanticModel:
        return cls.schema.model_validate(db_model)
    
    @classmethod
    def map_to_persistence_entity(cls, schema: BasePydanticModel) -> Base:
        return cls.db_model(**schema.model_dump())
    