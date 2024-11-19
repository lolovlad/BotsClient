from aiogram.fsm.state import State, StatesGroup


class FSMBot(StatesGroup):
    set_filter = State()
    get_reserve = State()
    chat_n = State()
