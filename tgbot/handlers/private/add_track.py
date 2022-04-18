import logging

from contextlib import suppress
from functools import lru_cache
from aiogram import F, Router, types, Bot
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
from aiohttp import ClientSession

from tgbot.handlers.private.profile import to_profile
from tgbot.keyboards.inline.profile import ProfileCallbackFactory
from tgbot.keyboards.inline.add_track import (
    AddSizesCallbackFactory,
    ShopCallbackFactory,
    get_cancel_kb,
    get_shops_kb,
    get_with_sizes_kb,
    get_without_sizes_kb,
    AddTrackCallbackFactory
)
from tgbot.misc.const import WB_URL
from tgbot.misc.repository import Repo
from tgbot.services.wildberries.get_info import get_product_info
from tgbot.states.add_track import AddTrackSG

router = Router()
logger = logging.getLogger(__name__)


@router.callback_query(ProfileCallbackFactory.filter(F.action == 'add_track'))
async def on_add_track(call: types.CallbackQuery, repo: Repo, state: FSMContext):
    shops = await repo.get_shops()

    await call.message.edit_text(
        '🏬 Выберите магазин:',
        reply_markup=get_shops_kb(shops)
    )

    if await state.get_state():
        await state.clear()


@router.callback_query(ShopCallbackFactory.filter())
async def on_select_shop(call: types.CallbackQuery, callback_data: ShopCallbackFactory, state: FSMContext):
    await call.message.edit_text(
        f'{callback_data.name}\n'
        'Введите уникальный ID (артикул) товара.\n\n'
        '<b>Пример:</b>\n'
        '<i>Wildberries</i> - <b>15875673</b>\n'
        '<i>Lamoda</i> - <b>MP002XM20VVQ</b>\n\n'
        '<i>Где найти артикул товара? - /help</i>',
        reply_markup=get_cancel_kb()
    )

    data = {
        'shop_id': callback_data.id,
        'shop_name': callback_data.name,
        'msg_id': call.message.message_id
    }

    await state.set_state(AddTrackSG.input_vendore_code)
    await state.update_data(data)


@lru_cache
@router.message(state=AddTrackSG.input_vendore_code)
async def on_input_vendore_code(
        message: types.Message,
        state: FSMContext,
        client_session: ClientSession,
        bot: Bot):
    data = await state.get_data()
    shop_id = data['shop_id']
    shop_name = data['shop_name']

    try:
        brand, name, price, sizes = await get_product_info(message.text, client_session, message.from_user.id)
    except TypeError:
        await message.answer('Немогу найти данный товар, попробуй ввести артикул еще раз')
        return

    text = [
        f'<b>Краткая информация</b>\n\n',
        f'<b>Название:</b>\n',
        f'└» <a href="{WB_URL.format(message.text)}">{brand} | {name}</a>\n',
        f'<b>Текущая цена:</b>\n',
        f'└» <code>{price:,}</code> ₽\n',
        f'<b>Артикул:</b>\n',
        f'└» <code>{message.text}</code>\n',
    ]
    await state.update_data(
        text=text,
        brand=brand,
        name=name,
        price=price,
        vendore_code=message.text
    )

    if len(sizes) > 1:
        keyboard = get_with_sizes_kb(sizes, shop_id, shop_name)
        disable_web_page_preview = True
        text.append(f'\n<b>Выберите размер</b>')
    else:
        keyboard = get_without_sizes_kb(
            shop_id,
            shop_name,
        )
        disable_web_page_preview = False
        text.insert(0, f'{shop_name} | {"Товар в наличии" if sizes[0][2] else "Товар отсутствует"}\n\n')

        await state.update_data(
            size_name=sizes[0][0],
            option_id=sizes[0][1],
            stocks=bool(sizes[0][2])
        )

    await message.answer(
        ''.join(text),
        reply_markup=keyboard,
        disable_web_page_preview=disable_web_page_preview
    )

    msg_id = data['msg_id']
    with suppress(TelegramBadRequest):
        await message.delete()
        await bot.delete_message(message.from_user.id, msg_id)


@router.callback_query(AddSizesCallbackFactory.filter(), state=AddTrackSG.input_vendore_code)
async def add_size(call: types.CallbackQuery, callback_data: AddSizesCallbackFactory, state: FSMContext):
    data = await state.get_data()
    text: list = data['text']

    text.insert(
        0,
        f'{callback_data.shop_name} | {"Товар в наличии" if callback_data.stocks else "Товар отсутствует"}\n\n'
    )
    text.extend(
        [
            f'<b>Размер:</b>\n',
            f'└» <code>{callback_data.size_name}</code>'
        ]
    )

    await call.message.edit_text(
        ''.join(text),
        reply_markup=get_without_sizes_kb(data['shop_id'], data['shop_name'])
    )

    await state.update_data(
        size_name=callback_data.size_name,
        option_id=callback_data.option_id,
        stocks=callback_data.stocks,
    )


@router.callback_query(AddTrackCallbackFactory.filter())
async def add_track(
        call: types.CallbackQuery,
        state: FSMContext,
        callback_data: AddTrackCallbackFactory,
        repo: Repo):
    data = await state.get_data()
    try:
        user = await repo.get_user(call.from_user.id)
        if user:
            user_track_exists = filter(
                lambda track: track.vendore_code == data['vendore_code'] and track.option_id == data['option_id'],
                user.tracks
            )
            if list(user_track_exists):
                await call.answer('У вас уже есть этот товар')
                return

        await repo.add_track(
            brand=data['brand'],
            name=data['name'],
            price=data['price'],
            vendore_code=data['vendore_code'],
            size_name=data.get('size_name'),
            option_id=data.get('option_id'),
            stocks=data.get('stocks'),
            shop_name=callback_data.shop_name,
            user_id=call.from_user.id
        )
        await call.answer(
            'Успешно !\n'
            'Вы добавили этот товар в мониторинг\n'
            'Я уведомлю вас, когда цена на товар снизится',
            show_alert=True
        )
    except Exception as err:
        logger.error(err)
        await call.answer('Что-то пошло не так, попробуйте позже')
    finally:
        await to_profile(call, repo)
        await state.clear()
