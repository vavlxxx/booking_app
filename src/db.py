from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from src.config import get_settings

engine = create_async_engine(get_settings().DB_URL)
async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)

engine_null_pool = create_async_engine(get_settings().DB_URL, poolclass=NullPool)
async_session_maker_null_pool = async_sessionmaker(bind=engine_null_pool, expire_on_commit=False)


class Base(DeclarativeBase):
    pass
