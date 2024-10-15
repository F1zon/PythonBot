from aiogram import html, Router, types, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from datetime import date
import datetime
from collections import defaultdict
import sqlite3 as sq

user_private_router = Router()

event = defaultdict(list)
tmp = []

@user_private_router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")
    db = sq.connect('tg.db')
    cur = db.cursor()
    # TODO: Испраить ввод данных в бд
    cur.execute(''' INSERT INTO users(chat_id) VALUES(?) ''', str(message.from_user.id))
    db.commit()
    db.close()


@user_private_router.message(Command('see_date_now'))
async def seeYesterday(message: Message) -> None:
    if str(date.today()) in event.keys():
        await message.answer("События на сегодня:")
        for i in event.get(str(date.today())):
            await message.answer(f"{i}\n")
    else:
        await message.answer("Событий на сегодня нет!")

@user_private_router.message(Command('see_date_tomorrow'))
async def seeTomorrow(message: types.Message):
    today = datetime.date.today()
    tomorrow = str(today + datetime.timedelta(days=1))
    if tomorrow in event.keys():
        await message.answer("События на завтра:")
        for i in event.get(tomorrow):
            await message.answer(f"{i}\n")
    else:
        await message.answer("Событий на зватра нет!")

@user_private_router.message(Command('add_date'))
async def getEvent(message: types.Message):
    await message.answer("Введите данные: гггг-мм-дд / описание")

@user_private_router.message(F.text.lower())
async def getMessageInEvent(message: types.Message):
    tmp = message.text.split(" / ")
    event[tmp[0]].append(tmp[1])
    await message.answer(f"Введённая дата: {tmp[0]}\nВведённое описание: {tmp[1]}")
    tmp = {}
   


