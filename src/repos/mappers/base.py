from typing import TypeVar

from src.schemas.base import BasePydanticModel
from src.db import Base

SchemaType = TypeVar("SchemaType", bound=BasePydanticModel)
DBModelType = TypeVar("DBModelType", bound=Base)


class DataMapper:
    db_model: DBModelType = None
    schema: SchemaType = None

    @classmethod
    def map_to_domain_entity(cls, db_model: DBModelType) -> SchemaType:
        return cls.schema.model_validate(db_model)
    
    @classmethod
    def map_to_persistence_entity(cls, schema: SchemaType) -> DBModelType:
        return cls.db_model(**schema.model_dump())
    