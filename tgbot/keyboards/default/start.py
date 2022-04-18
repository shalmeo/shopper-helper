from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder 


def get_start_kb():
    builder = ReplyKeyboardBuilder()
    
    builder.row(KeyboardButton(text='🏠 Профиль'), KeyboardButton(text='📎 Информация'))
    
    return builder.as_markup(resize_keyboard=True)
    
    