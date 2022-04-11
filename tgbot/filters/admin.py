from aiogram import types
from aiogram.dispatcher.filters import BaseFilter

from tgbot.config import Config


class AdminFilter(BaseFilter):
        
    async def __call__(self, message: types.Message, config: Config) -> bool:
        return message.from_user.id in config.bot.admin_ids
