from aiogram.filters.callback_data import CallbackData


class TypeFilterCallback(CallbackData, prefix='type'):
    id_type: int


class RegionFilterCallback(CallbackData, prefix='region'):
    id_region: int

