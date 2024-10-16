from aiogram import html, Router, types, F
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

from datetime import date
import datetime
from collections import defaultdict
import sqlite3 as sq
import string
import logging

user_private_router = Router()
tmp = {}

class FSMFillForm(StatesGroup):
    fill_date = State()
    fill_desc = State()
    fill_dateToDate = State()


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
    descList = getDescForDate(getDateYesterday(), str(message.from_user.id))
    if len(descList) < 0:
        await message.answer("Событий на сегодня нет!")
        return
    
    await message.answer("События на сегодня:")
    for i in descList:
        await message.answer(getStr(i))


@user_private_router.message(Command('see_date_tomorrow'))
async def seeTomorrow(message: types.Message):
    descList = getDescForDate(getDateTomorrow(), str(message.from_user.id))
    if len(descList) < 0:
        await message.answer("Событий на завтра нет!")
        return

    await message.answer("События на завтра:")
    for i in descList:
        await message.answer(getStr(i))


@user_private_router.message(Command('see_date_by_date'))
async def seeByDate(message: types.Message, state: FSMContext):
    await message.answer("Введите дату формата ГГГГ-ММ-ДД")
    await state.set_state(FSMFillForm.fill_date)


@user_private_router.message(StateFilter(FSMFillForm.fill_date))
async def getDateByEv(message: types.Message, state: FSMContext):
    await state.update_data(dates=message.text)
    tmp = await state.get_data()
    await state.clear()

    datus = tmp.get('dates')
    tmp.clear()

    descList = getDescForDate(datus, str(message.from_user.id))
    if len(descList) < 0:
        await message.answer(f"Событий по дате {datus} нет!")
        return
    
    await message.answer(f"События по дате {datus}:")
    for i in descList:
        await message.answer(getStr(i))

@user_private_router.message(Command('add_date'))
async def getEvent(message: types.Message, state: FSMContext):
    # await message.answer("Введите данные: ГГГГ-ММ-ДД")
    await message.answer("Введите данные: ДД.ММ.ГГГГ")
    await state.set_state(FSMFillForm.fill_dateToDate)


@user_private_router.message(StateFilter(FSMFillForm.fill_dateToDate))
async def setDescEvent(message: types.Message, state: FSMContext):
    await state.update_data(dates=message.text)
    await message.answer("Введите название события")
    await state.set_state(FSMFillForm.fill_desc)


@user_private_router.message(StateFilter(FSMFillForm.fill_desc))
async def setInfo(message: types.Message, state: FSMContext):
    await state.update_data(desc=message.text)
    tmp = await state.get_data()
    await state.clear()
    await message.answer("Спасибо, Данные введены!")

    addDate(tmp.get('dates'), tmp.get('desc'), str(message.from_user.id))
    await message.answer("Введённые данные")
    await message.answer(f"Дата = {tmp.get('dates')}")
    await message.answer(f"Событие = {tmp.get('desc')}")
    tmp.clear()


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


def getDateYesterday():
    datusArr = str(date.today()).split("-")
    result = f"{datusArr[2]}.{datusArr[1]}.{datusArr[0]}"

    return result


def getDateTomorrow():
    today = datetime.date.today()
    tomorrow = str(today + datetime.timedelta(days=1))

    datusArr = tomorrow.split("-")
    result = f"{datusArr[2]}.{datusArr[1]}.{datusArr[0]}"

    return result
