from aiogram.dispatcher.fsm.state import StatesGroup, State


class AddTrackSG(StatesGroup):
    input_vendore_code = State()