from aiogram.types.user import User as TelegramUser
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from uuid import uuid4

from tgbot.services.database.models import Shop, Track, User


class Repo:
    def __init__(self, session: AsyncSession):
        self.session = session

    # users
    async def add_user(self, telegram_user: TelegramUser) -> User:
        user = await self.session.merge(
            User(
                id=telegram_user.id,
                full_name=telegram_user.full_name,              
            )
        )
        
        await self.session.commit()
        return user

    async def list_users(self) -> list[User]:
        users = await self.session.scalars(select(User))
        
        return users.all()
    
    async def get_user(self, user_id: int) -> User:
        user = await self.session.scalar(
            select(
                User
            ).where(
                User.id == user_id
            ).options(
                selectinload(User.tracks)
            )
        )

        return user
    
    # shops
    async def get_shops(self) -> list[Shop]:
        shops = await self.session.scalars(
            select(Shop)
        )
        
        return shops.all()

    #tracks
    async def add_track(
            self, brand: str, name: str,
            price: int, vendore_code: str, size_name: str,
            option_id: int, stocks: bool, shop_name: str, user_id: int) -> None:

        await self.session.merge(
            Track(
                id=str(uuid4()),
                brand=brand,
                name=name,
                price=price,
                vendore_code=vendore_code,
                size_name=size_name,
                option_id=option_id,
                stocks=stocks,
                shop=shop_name,
                user_id=user_id
            )
        )

        await self.session.commit()

    async def get_track(self, track_id) -> Track:
        track = await self.session.get(Track, track_id)

        return track

    async def delete_track(self, track_id) -> None:
        await self.session.execute(delete(Track).where(Track.id == track_id))

        await self.session.commit()
