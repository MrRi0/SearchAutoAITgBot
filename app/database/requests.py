from app.database.models import async_session
from app.database.models import User, Item
from sqlalchemy import select, delete

import app.car_ad as car

async def set_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()

async def add_item(tg_id, ad: car.CarAd):
    async with async_session() as session:
        item = await session.scalar(select(Item).where(Item.user_tg_id == tg_id).where(Item.url == ad.url))

        if not item:
            session.add(Item(
                name=ad.auto_name,
                price=ad.price,
                engine=ad.engine,
                fuel=ad.fuel,
                gearbox=ad.gearbox,
                drive_type=ad.drive_type,
                mileage=ad.mileage,
                url=ad.url,
                photo_url=ad.photo,
                user_tg_id=tg_id))
            await session.commit()

async def get_items(tg_id):
    async with async_session() as session:
        return await session.scalars(select(Item).where(Item.user_tg_id == tg_id))

async def get_item(id):
    async with async_session() as session:
        return await session.scalar(select(Item).where(Item.id == id))

async def delete_item(id):
    async with async_session() as session:
        item = await session.scalar(select(Item).where(Item.id == id))
        if item:
            await session.delete(item)
            await session.commit()