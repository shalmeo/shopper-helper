from aiogram import Router, types

from tgbot.keyboards.default.start import get_start_kb
from tgbot.misc.repository import Repo


router = Router()


@router.message(commands=['start'], state='*')
async def on_start(message: types.Message, repo: Repo):
    await message.answer(
        'Приветствую тебя 👋\n\n'
        'Я помогу тебе мониторить разные товарчики с крупных интернет мазагинов\n'
        'Начинай мониторить 🛍',
        reply_markup=get_start_kb()
    )
    
    user = await repo.get_user(message.from_user.id)
    
    if not user: 
        await repo.add_user(message.from_user)
