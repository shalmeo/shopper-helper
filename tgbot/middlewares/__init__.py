from aiogram import Dispatcher

from .database import DBSession
from .acl import AclMiddleware
from .throttling import ThrottlingMiddleware


def setup(dp: Dispatcher, session_pool):
    # dp.message.outer_middleware(DBSession(session_pool))
    # dp.callback_query.outer_middleware(DBSession(session_pool))
    #
    # dp.message.outer_middleware(AclMiddleware())
    # dp.callback_query.outer_middleware(AclMiddleware())
    #
    dp.message.middleware(ThrottlingMiddleware())