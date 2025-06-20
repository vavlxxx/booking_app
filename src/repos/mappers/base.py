from src.schemas.base import BasePydanticModel


class DataMapper:
    db_model = None
    schema = None

    @classmethod
    def map_to_domain_entity(cls, db_model):
        return cls.schema.model_validate(db_model)
    
    @classmethod
    def map_to_persistence_entity(cls, schema):
        return cls.db_model(**schema.model_dump())
    