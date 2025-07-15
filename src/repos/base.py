import logging

from typing import Any, Sequence

from asyncpg import UniqueViolationError, DataError
from sqlalchemy import delete, select, insert, update
from sqlalchemy.exc import NoResultFound, IntegrityError, DBAPIError
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import Base
from src.schemas.base import BasePydanticModel
from src.repos.mappers.base import DataMapper
from src.utils.exceptions import (
    ObjectNotFoundException,
    ObjectAlreadyExistsException,
    InvalidDataException
)

class BaseRepository:

    model: type[Base]
    mapper: type[DataMapper]
    session: AsyncSession

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_filtered(self, *filter, **filter_by) -> list[BasePydanticModel | Any]:
        query = (
            select(self.model)
            .filter(*filter)
            .filter_by(**filter_by)
        )
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(obj) for obj in result.scalars().all()]


    async def get_all(self) -> list[BasePydanticModel]:
        return await self.get_all_filtered()


    async def get_one_or_none(self, **filter_by) -> BasePydanticModel | None| Any:
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        obj = result.scalars().one_or_none()
        if obj is None:
            return None
        return self.mapper.map_to_domain_entity(obj) 


    async def get_one(self, **filter_by) -> BasePydanticModel | Any:
        query = select(self.model).filter_by(**filter_by)
        try:
            result = await self.session.execute(query)
            obj = result.scalar_one()
        except NoResultFound:
            raise ObjectNotFoundException
        except DBAPIError as exc:
            logging.error(f"Cannot get data from DB, {filter_by=}, exc_type={exc.orig}")
            if isinstance(exc.orig.__cause__, DataError): # type: ignore
                raise InvalidDataException from exc
            logging.error("Unknown unhandled exception")
            raise exc

        return self.mapper.map_to_domain_entity(obj) 


    async def add_bulk(self, data: Sequence[BasePydanticModel]):
        add_obj_stmt = insert(self.model).values([item.model_dump() for item in data])
        await self.session.execute(add_obj_stmt)


    async def add(self, data: BasePydanticModel, **params):
        add_obj_stmt = insert(self.model).values(**data.model_dump(), **params).returning(self.model)
        try:
            result = await self.session.execute(add_obj_stmt)
        except IntegrityError as exc:
            logging.error(f"Cannot insert data into DB, {data=}, exc_type={exc.orig}")
            if isinstance(exc.orig.__cause__, UniqueViolationError): # type: ignore
                raise ObjectAlreadyExistsException from exc
            logging.error("Unknown unhandled exception")
            raise exc

        obj = result.scalars().one()
        return self.mapper.map_to_domain_entity(obj)


    async def edit(self, data: BasePydanticModel, exclude_unset=True, exclude_fields=None, **filter_by):
        exclude_fields = exclude_fields or set()
        
        to_update = data.model_dump(
            exclude=exclude_fields, 
            exclude_unset=exclude_unset
        )

        if not to_update:
            return

        edit_obj_stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**to_update)
        )

        try:
            result = await self.session.execute(edit_obj_stmt)
        except IntegrityError as exc:
            logging.error(f"Cannot update data in DB, {data=}, exc_type={exc.orig}")
            if isinstance(exc.orig.__cause__, UniqueViolationError): # type: ignore
                raise ObjectAlreadyExistsException from exc
            logging.error("Unknown unhandled exception")
            raise exc


    async def delete(self, *filter, **filter_by):
        delete_obj_stmt = (
            delete(self.model)
            .filter(*filter)
            .filter_by(**filter_by)
        )
        await self.session.execute(delete_obj_stmt)
    