import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.connectors.redis_manager import RedisManager
from src.config import get_settings


redis_manager = RedisManager(
    host=get_settings().REDIS_HOST, 
    port=get_settings().REDIS_PORT
)
