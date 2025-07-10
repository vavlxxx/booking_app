from src.utils.db_manager import DBManager


class BaseService:
    db: DBManager 

    def __init__(self, db: DBManager) -> None:
        self.db = db
    
    @staticmethod
    def _db_required(func):
        async def wrapper(*args, **kwargs):
            self = args[0]
            if self.db is None:
                raise ValueError("db attibute is not initialized, please provide the \'DBManager\' instance to the service")
            return await func(*args, **kwargs)
        return wrapper
    
