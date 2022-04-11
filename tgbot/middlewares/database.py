from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.orm import sessionmaker


class DBSession(BaseMiddleware):
    def __init__(self, session_pool: sessionmaker) -> None:
        self.session = session_pool

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:

        async with self.session() as session:
            data['session'] = session

            result = await handler(event, data)

            data.pop('session')
            return result