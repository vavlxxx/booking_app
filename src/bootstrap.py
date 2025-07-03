import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.connectors.redis_manager import RedisManager
from src.config import settings


redis_manager = RedisManager(
    host=settings.REDIS_HOST, 
    port=settings.REDIS_PORT
)
