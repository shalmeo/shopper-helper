import logging

from contextlib import suppress
from aiogram import F, Router, types, Bot
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.keyboards.inline.list_tracks import (
    get_list_tracks_kb,
    TrackCallbackFactory,
    get_track_kb,
    ChangeTrackCallbackFactory, get_change_threshold_kb
)
from tgbot.keyboards.inline.profile import ProfileCallbackFactory
from tgbot.misc.const import WB_URL
from tgbot.misc.repository import Repo
from tgbot.services.database.models import Track
from tgbot.states.change_threshold import ChangeThresholdSG

router = Router()
logger = logging.getLogger(__name__)


@router.callback_query(ProfileCallbackFactory.filter(F.action == 'get_list_tracks'))
async def on_list_tracks(call: types.CallbackQuery, repo: Repo):
    user = await repo.get_user(call.from_user.id)
    await call.message.edit_text(
        '📝 Список товаров:',
        reply_markup=get_list_tracks_kb(user.tracks)
    )


@router.callback_query(TrackCallbackFactory.filter(), state='*')
async def on_track(
        obj: types.CallbackQuery | types.Message,
        repo: Repo,
        callback_data: TrackCallbackFactory | str,
        state: FSMContext):

    track_id = callback_data
    if isinstance(callback_data, TrackCallbackFactory):
        track_id = callback_data.id

    track = await repo.get_track(track_id)
    text = [
        f'{track.shop} | {"Товар в наличии" if track.stocks else "Товар отсутствует"}\n\n',
        f'<b>Название:</b>\n',
        f'└» <a href="{WB_URL.format(track.vendore_code)}">{track.brand} | {track.name}</a>\n',
        f'<b>Текущая цена:</b> \n',
        f'└» <code>{track.price:,}</code> ₽\n',
        f'<b>Артикул:</b>\n',
        f'└» <code>{track.vendore_code}</code>\n',
        f'<b>Порог цены:</b>\n',
        f'└» {f"<code>{track.threshold:,}</code> ₽" if track.threshold else "Любое изменение"}\n'
    ]

    if track.size_name != "0":
        text.extend([
            f'<b>Размер:</b>\n',
            f'└» <code>{track.size_name}</code>'
        ])

    if isinstance(obj, types.CallbackQuery):
        await obj.message.edit_text(
            ''.join(text),
            reply_markup=get_track_kb(track_id)
        )
    else:
        await obj.answer(
            ''.join(text),
            reply_markup=get_track_kb(track_id)
        )

    if await state.get_state():
        await state.clear()


@router.callback_query(ChangeTrackCallbackFactory.filter(F.action == 'del'))
async def on_delete_track(call: types.CallbackQuery, callback_data: ChangeTrackCallbackFactory, repo: Repo):
    try:
        await repo.delete_track(callback_data.id)
        await call.answer('Товар был успешно удален !', show_alert=True)
    except Exception as err:
        await call.answer('Что-то пошло не так, попробуйте позже')
        logger.error(err)
    finally:
        await on_list_tracks(call, repo)


@router.callback_query(ChangeTrackCallbackFactory.filter(F.action == 'chg'))
async def on_change_threshold(
        call: types.CallbackQuery,
        callback_data: ChangeTrackCallbackFactory,
        state: FSMContext):
    msg = await call.message.edit_text(
        '⚙️ Введите порог цены.\n\n'
        'Если цена упадет ниже порога, то я уведомлю вас о снижении.\n'
        'По умолчанию я буду уведомлять вас при каждом изменении цены.',
        reply_markup=get_change_threshold_kb(callback_data.id)
    )

    await state.set_state(ChangeThresholdSG.input_threshold)
    await state.update_data(track_id=callback_data.id, msg_id=msg.message_id)


@router.message(state=ChangeThresholdSG.input_threshold)
async def input_threshold(message: types.Message, state: FSMContext, session: AsyncSession, bot: Bot, repo: Repo):
    try:
        data = await state.get_data()
        track = await session.get(Track, data['track_id'])
        new_threshold = int(message.text)
        track.threshold = new_threshold
        if track.price < new_threshold:
            await message.answer('<b>Похоже, вы ввели значение большее чем текущая цена</b>')
        if new_threshold < 0 :
            await message.answer('<b>Минимальная цена для отслеживания товара <code>0</code> ₽</b>')

        await session.commit()
    except ValueError:
        await message.answer(
            '<b>Цена должна быть целым числом</b>'
        )
    finally:
        await state.clear()
        msg_id = data['msg_id']
        with suppress(TelegramBadRequest):
            await message.delete()
            await bot.delete_message(message.from_user.id, msg_id)
        await on_track(message, repo, data['track_id'], state)