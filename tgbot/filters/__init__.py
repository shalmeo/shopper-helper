from aiogram import Dispatcher

from .admin import AdminFilter 


def setup(dp: Dispatcher):
    dp.message.bind_filter(AdminFilter)