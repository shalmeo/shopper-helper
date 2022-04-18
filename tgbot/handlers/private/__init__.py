from . import add_track, start, profile, list_tracks

from aiogram import Router


def setup(master_router: Router):
    for module in (start, profile, add_track, list_tracks):
        master_router.include_router(module.router)

