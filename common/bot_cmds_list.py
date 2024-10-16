from aiogram.types import BotCommand

private = [
    BotCommand(command='add_date', description='Добавить дату'),
    BotCommand(command='see_date_now', description='посмотреть события на сегодня'),
    BotCommand(command='see_date_tomorrow', description='посмотреть события на завтра'),
    BotCommand(command='see_date_by_date', description='посмотреть событие по дате')
]