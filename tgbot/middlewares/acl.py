from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, CallbackQuery, Message

from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.services.database.models import User


class AclMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: Message | CallbackQuery,
            data: Dict[str, Any]
    ) -> Any:
        session: AsyncSession = data['session']
        telegram_user = event.from_user     
        
        user = await session.get(User, telegram_user.id)
        
        if user is None:
            user = await session.merge(
                User(id=telegram_user.id,
                     full_name=telegram_user.full_name)
            )
            await session.commit()
        
        data['user'] = user
        
        result = await handler(event, data)
        
        data.pop('user')
        return result