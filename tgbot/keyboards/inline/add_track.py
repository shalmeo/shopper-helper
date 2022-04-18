from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.dispatcher.filters.callback_data import CallbackData
from tgbot.keyboards.inline.profile import ProfileCallbackFactory

from tgbot.services.database.models import Shop


class ShopCallbackFactory(CallbackData, prefix='shop'):
    id: str
    name: str


class AddSizesCallbackFactory(CallbackData, prefix='add_sizes'):
    size_name: str
    option_id: int
    stocks: bool
    shop_id: str
    shop_name: str


class AddTrackCallbackFactory(CallbackData, prefix='add_track'):
    shop_name: str
    shop_id: str


def get_shops_kb(shops: list[Shop]):
    builder = InlineKeyboardBuilder()
    
    for shop in shops:
        builder.row(InlineKeyboardButton(text=shop.name, callback_data=ShopCallbackFactory(id=shop.id, name=shop.name).pack()))
    
    builder.row(InlineKeyboardButton(text='🏠 Профиль', callback_data='to_profile'))
    
    return builder.as_markup()


def get_cancel_kb():
    builder = InlineKeyboardBuilder()
   
    builder.row(InlineKeyboardButton(text='⬅️ Назад', callback_data=ProfileCallbackFactory(action='add_track').pack()))
    
    return builder.as_markup()


def get_without_sizes_kb(shop_id, shop_name):
    builder = InlineKeyboardBuilder()
    
    builder.row(
        InlineKeyboardButton(
            text='🖲 Отслеживать',
            callback_data=AddTrackCallbackFactory(
                shop_name=shop_name,
                shop_id=shop_id
            ).pack()
        )
    )
    builder.row(
        InlineKeyboardButton(
            text='⬅️ Назад',
            callback_data=ShopCallbackFactory(
                id=shop_id,
                name=shop_name
            ).pack()
        )
    )

    return builder.as_markup()


def get_with_sizes_kb(sizes, shop_id, shop_name):
    builder = InlineKeyboardBuilder()
    
    for size in sizes:
        size_name, option_id, stocks = size
        
        builder.add(
            InlineKeyboardButton(
                text=size_name,
                callback_data=AddSizesCallbackFactory(
                    size_name=size_name,
                    option_id=option_id,
                    stocks=bool(stocks),
                    shop_id=shop_id,
                    shop_name=shop_name
                ).pack()
            )
        )
    
    builder.adjust(4)
    
    builder.row(
        InlineKeyboardButton(
            text='⬅️ Назад',
            callback_data=ShopCallbackFactory(
                id=shop_id,
                name=shop_name
            ).pack()
        )
    )
    
    return builder.as_markup()