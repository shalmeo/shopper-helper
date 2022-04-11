from aiogram import Router

from . import admin, echo
from tgbot.filters.admin import AdminFilter


def setup(master_router: Router):
    router = Router()
    router.message.filter(AdminFilter())
    router.callback_query.filter(AdminFilter())
    
    for module in (admin, echo):
        router.include_router(module.router)
    
    master_router.include_router(router)
    
       