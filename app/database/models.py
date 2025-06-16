from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3')

async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)

class Item(Base):
    __tablename__ = 'items'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    price: Mapped[str] = mapped_column(String(30))
    engine: Mapped[str] = mapped_column(String(30))
    fuel: Mapped[str] = mapped_column(String(30))
    gearbox: Mapped[str] = mapped_column(String(30))
    drive_type: Mapped[str] = mapped_column(String(30))
    mileage: Mapped[str] = mapped_column(String(30))
    photo_url: Mapped[str] = mapped_column(String(500))
    url: Mapped[str] = mapped_column(String(500))
    user_tg_id: Mapped[BigInteger] = mapped_column(ForeignKey('users.tg_id'))

async def async_main():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

