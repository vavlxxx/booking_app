from src.services.base import BaseService
from src.schemas.additionals import AdditionalsRequest
from src.utils.exceptions import ObjectAlreadyExistsException, AdditionalAlreadyExistsException


class AdditionalsService(BaseService):
    async def add_additional(self, additional_data: AdditionalsRequest):
        try:
            additional = await self.db.additionals.add(additional_data)
        except ObjectAlreadyExistsException as exc:
            raise AdditionalAlreadyExistsException from exc

        await self.db.commit()
        return additional

    async def get_additionals(self):
        additionals = await self.db.additionals.get_all()
        return additionals
