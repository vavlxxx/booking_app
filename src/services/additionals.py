from src.services.base import BaseService
from src.schemas.additionals import AdditionalsRequest


class AdditionalsService(BaseService):
    
    async def add_additional(self, additional_data: AdditionalsRequest):
        additional = await self.db.additionals.add(additional_data)
        await self.db.commit()
        return additional
    

    async def get_additionals(self):
        additionals = await self.db.additionals.get_all()
        return additionals
    