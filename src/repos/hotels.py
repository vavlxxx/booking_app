from sqlalchemy import select, func

from src.schemas.hotels import Hotel
from src.repos.base import BaseRepository
from src.models.hotels import HotelsOrm


class HotelsRepository(BaseRepository):

    model = HotelsOrm
    schema = Hotel

    async def get_all(
        self,
        location,
        title,
        limit,
        offset,
    ) -> list[Hotel]:
        query = select(HotelsOrm)

        if location:
            query = query.filter(
                func.lower(HotelsOrm.location).contains(location.strip().lower())
            )
        if title:
            query = query.filter(
                func.lower(HotelsOrm.title).contains(title.strip().lower())
            )

        query = query.limit(limit).offset(offset)
        result = await self.session.execute(query)
        return [self.schema.model_validate(hotel) for hotel in result.scalars().all()]
