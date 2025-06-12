from typing import Annotated
from pydantic import BaseModel
from fastapi import Depends, Query


class PaginationParams(BaseModel):
    
    page: Annotated[int | None, Query(
        default=1, 
        ge=1, 
        description="Номер страницы"
        )]
    
    per_page: Annotated[int | None, Query(
        default=5, 
        ge=1, 
        le=10, 
        description="Количество отелей на странице"
        )]

PaginationDep = Annotated[PaginationParams, Depends()]
