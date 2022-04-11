import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.dispatcher.fsm.storage.memory import MemoryStorage
from aiogram.dispatcher.fsm.storage.redis import RedisStorage

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from tgbot.config import load_config
from tgbot.misc.set_bot_commands import set_dafault_commands
from tgbot.services.database.utils import get_connection_string
from tgbot import middlewares, filters, handlers


logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")
    config = load_config(".env")
    
    engine = create_async_engine(
        get_connection_string(config.db), future=True, echo=False
    )

    session_pool = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    # Creating
    if config.bot.use_redis:
        storage = RedisStorage.from_url(
            url=f'redis://{config.redis.host}:{config.redis.port}'
        )
    else:
        storage = MemoryStorage()

    bot = Bot(token=config.bot.token, parse_mode='HTML')
    dp = Dispatcher(storage=storage)

    # setup
    middlewares.setup(dp, session_pool)
    filters.setup(dp)
    handlers.setup(dp)

    # set commands
    await set_dafault_commands(bot)
    
    try:
        await bot.get_updates(offset=-1)
        await dp.start_polling(bot, config=config)
    finally:
        await storage.close()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
