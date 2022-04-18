from aiogram import Router, types
from tgbot.misc.profile_text import get_profile_text

from tgbot.misc.repository import Repo
from tgbot.keyboards.inline.profile import get_profile_kb


router = Router()


@router.message(text='🏠 Профиль', state='*')
async def on_profile(message: types.Message, repo: Repo):
    user = await repo.get_user(message.from_user.id)
    text = get_profile_text(message.from_user.id, len(user.tracks))
    await message.answer(
        ''.join(text),
        reply_markup=get_profile_kb()
    )


@router.callback_query(text='to_profile')
async def to_profile(call: types.CallbackQuery, repo: Repo):
    user = await repo.get_user(call.from_user.id)
    text = get_profile_text(call.from_user.id, len(user.tracks))
    await call.message.edit_text(
        ''.join(text),
        reply_markup=get_profile_kb()
    )
