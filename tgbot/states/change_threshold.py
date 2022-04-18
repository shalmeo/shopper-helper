from aiogram.dispatcher.fsm.state import StatesGroup, State


class ChangeThresholdSG(StatesGroup):
    input_threshold = State()
