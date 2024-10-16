from aiogram import html, Router, types, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from datetime import date
import datetime
from collections import defaultdict
import sqlite3 as sq
import string
import logging

user_private_router = Router()
tmp = []

@user_private_router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")
    db = sq.connect('tg.db')
    cur = db.cursor()
    chatId = str(message.from_user.id)

    cur.execute(f"SELECT chat_id from users where chat_id = {chatId}")
    userList = cur.fetchall()
    if len(userList) < 1:
        cur.execute(f"INSERT INTO users(chat_id) VALUES({chatId})")
        db.commit()

    cur.execute(f"SELECT chat_id from users where chat_id = {chatId}")
    user = cur.fetchall()

    if len(user) > 1:
        cur.execute(f"DELETE FROM users WHERE chat_id = {chatId}")
        cur.execute(f"INSERT INTO users(chat_id) VALUES({chatId})")
        db.commit()

    db.close()


@user_private_router.message(Command('see_date_now'))
async def seeYesterday(message: types.Message) -> None:
    descList = getDescForDate(str(date.today()), str(message.from_user.id))
    if len(descList) < 0:
        await message.answer("Событий на сегодня нет!")
        return
    
    await message.answer("События на сегодня:")
    for i in descList:
        await message.answer(getStr(i))

@user_private_router.message(Command('see_date_tomorrow'))
async def seeTomorrow(message: types.Message):
    today = datetime.date.today()
    tomorrow = str(today + datetime.timedelta(days=1))

    descList = getDescForDate(tomorrow, str(message.from_user.id))
    if len(descList) < 0:
        await message.answer("Событий на завтра нет!")
        return

    await message.answer("События на завтра:")
    for i in descList:
        await message.answer(getStr(i))

@user_private_router.message(Command('see_date_by_date'))
async def seeByDate(message: types.Message):
    await message.answer("Введите дату формата гггг-мм-дд")

@user_private_router.message(Command('add_date'))
async def getEvent(message: types.Message):
    await message.answer("Введите данные: гггг-мм-дд / описание")


@user_private_router.message(F.text.lower())
async def getMessageInEvent(message: types.Message):
    tmp = message.text.split(" / ")

    # Просмотр событий по дате
    if len(tmp) < 2:
        descList = getDescForDate(tmp[0], str(message.from_user.id))
        if len(descList) < 0:
            await message.answer("Событий по указанной дате нет!")
            return

        await message.answer(f"События по дате {tmp[0]}:")
        for i in descList:
            await message.answer(getStr(i))
        return

    addDate(tmp[0], tmp[1], str(message.from_user.id))
    logging.info(len(tmp))

    await message.answer(f"Введённая дата: {tmp[0]}\nВведённое описание: {tmp[1]}")
    tmp = {}


def getUser(chatId):
    db = sq.connect('tg.db')
    cur = db.cursor()

    cur.execute(f"SELECT chat_id from users where chat_id = {chatId}")
    userList = cur.fetchall()
    db.close()

    return getStr(str(userList[0]))


def getStr(strIn):
    strIn = str(strIn)
    tr = str.maketrans('', '', string.punctuation)
    return strIn.translate(tr)


def addDate(dates, desc, chatId):
    db = sq.connect('tg.db')
    cur = db.cursor()

    cur.execute("INSERT INTO events(desc, dates, chat_id) VALUES(?, ?, ?)", (desc, dates, chatId,))
    db.commit()
    db.close()


def getDescForDate(dates, chatId):
    db = sq.connect('tg.db')
    cur = db.cursor()

    cur.execute("SELECT desc FROM events WHERE dates = ? AND chat_id = ?", (dates, chatId,))
    descs = cur.fetchall()
    db.close()

    return descs
