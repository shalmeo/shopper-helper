from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.dispatcher.filters.callback_data import CallbackData


class ProfileCallbackFactory(CallbackData, prefix='profile'):
    action: str


def get_profile_kb():
    builder = InlineKeyboardBuilder()
    
    builder.row(InlineKeyboardButton(text='💠 Добавить товар', callback_data=ProfileCallbackFactory(action='add_track').pack()))
    builder.row(InlineKeyboardButton(text='📝 Список товаров', callback_data=ProfileCallbackFactory(action='get_list_tracks').pack()))
    
    return builder.as_markup()
    