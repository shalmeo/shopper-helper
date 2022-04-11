from . import start

from aiogram import Router


def setup(master_router: Router):
    for module in (start,):
        master_router.include_router(module.router)

