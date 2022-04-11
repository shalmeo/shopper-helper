from aiogram import Router, types


router = Router()


@router.message(commands=['start'], state='*')
async def start(message: types.Message):
    await message.answer('Hello user')