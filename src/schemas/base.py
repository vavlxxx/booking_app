from pydantic import BaseModel, ConfigDict


class BasePydanticModel(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        str_min_length=1,
    )  # type: ignore
