import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, html, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from config import TOKEN
from handlers.user_privet import user_private_router
from common.bot_cmds_list import private

ALLOWED_UPDATES = ['message, edited_message']
# Bot token can be obtained via https://t.me/BotFather
dp = Dispatcher()
dp.include_router(user_private_router)

async def main() -> None:
  bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
  await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
  await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)


if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO, stream=sys.stdout)
  asyncio.run(main())