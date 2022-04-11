from aiogram import Dispatcher, Router

from . import admin, private



def setup(dp: Dispatcher):
    master_router = Router()
    
    for module in (admin, private):
        module.setup(master_router)
    
    dp.include_router(master_router)