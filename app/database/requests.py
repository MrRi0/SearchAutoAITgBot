from app.database.models import async_session
from app.database.models import User, Item
from sqlalchemy import select

async def set_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()

async def add_item(tg_id, name, url):
    async with async_session() as session:
        item = await session.scalar(select(Item).where(Item.user_tg_id == tg_id).where(Item.url == url))

        if not item:
            session.add(Item(name=name, url=url, user_tg_id=tg_id))
            await session.commit()

async def get_items(tg_id):
    async with async_session() as session:
        return await session.scalars(select(Item).where(Item.user_tg_id == tg_id))
