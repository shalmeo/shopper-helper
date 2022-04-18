from enum import Enum
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.dispatcher.filters.callback_data import CallbackData

from tgbot.keyboards.inline.profile import ProfileCallbackFactory
from tgbot.services.database.models import Track


class TrackCallbackFactory(CallbackData, prefix='track'):
    id: str


class ChangeTrackCallbackFactory(CallbackData, prefix='change_track'):
    id: str
    action: str


def get_list_tracks_kb(tracks: list[Track]):
    builder = InlineKeyboardBuilder()
    
    for track in tracks:
        builder.row(
            InlineKeyboardButton(
                text=f'{track.brand} [{track.vendore_code}]',
                callback_data=TrackCallbackFactory(
                    id=track.id,
                ).pack()
            )
        )
    
    builder.row(InlineKeyboardButton(text='🏠 Профиль', callback_data='to_profile'))

    return builder.as_markup()


def get_track_kb(track_id):
    builder = InlineKeyboardBuilder()

    builder.add(
        InlineKeyboardButton(
            text='⚙️ Изменить порог',
            callback_data=ChangeTrackCallbackFactory(
                id=track_id,
                action='chg'
            ).pack()
        ),
        InlineKeyboardButton(
            text='🗑 Удалить',
            callback_data=ChangeTrackCallbackFactory(
                id=track_id,
                action='del'
            ).pack()
        ),
        InlineKeyboardButton(
            text='⬅️ Назад',
            callback_data=ProfileCallbackFactory(
                action='get_list_tracks'
            ).pack()
        ),
    )

    builder.adjust(1)

    return builder.as_markup()


def get_change_threshold_kb(track_id):
    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(
        text='Любое изменение',
        callback_data=ChangeTrackCallbackFactory(id=track_id, action='any_threshold').pack()
    ))

    builder.row(InlineKeyboardButton(
        text='⬅️ Назад',
        callback_data=TrackCallbackFactory(id=track_id).pack()
    ))

    return builder.as_markup()
