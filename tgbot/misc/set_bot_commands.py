from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats 


async def set_dafault_commands(bot: Bot):
    commands = [
        BotCommand(command='start', description='Старт')
    ]
    await bot.set_my_commands(commands=commands, scope=BotCommandScopeAllPrivateChats())