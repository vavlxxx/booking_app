import logging

import redis.asyncio as redis


class RedisManager:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    async def connect(self):
        logging.info(f"Beginning connection to Redis {self.host}:{self.port}")
        self._redis = await redis.Redis(host=self.host, port=self.port)
        logging.info(f"Successful connection to Redis {self.host}:{self.port}")

    async def set(self, key: str, value: str, expire: int | None = None):
        if expire:
            await self._redis.set(key, value, ex=expire)
            return
        await self._redis.set(key, value)

    async def get(self, key: str):
        return await self._redis.get(key)

    async def delete(self, key: str):
        return await self._redis.delete(key)

    async def close(self):
        if self._redis:
            await self._redis.close()
