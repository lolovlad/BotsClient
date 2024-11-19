from aiogram.filters.callback_data import CallbackData


class TypeCommandPagination(CallbackData, prefix='pagination'):
    type_pagination: str


class CommandCallback(CallbackData, prefix='command'):
    reserver_id: int | None
    type_command: str
