from aiogram import Dispatcher

from .database import DBSession
from .throttling import ThrottlingMiddleware


def setup(dp: Dispatcher, session_pool):
    dp.message.outer_middleware(DBSession(session_pool))
    dp.callback_query.outer_middleware(DBSession(session_pool))
    
    dp.message.middleware(ThrottlingMiddleware())