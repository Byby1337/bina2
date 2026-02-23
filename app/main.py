"""
Entry point для запуска бота как модуля `app.main`.

Важно: добавляем корень проекта в `sys.path`, чтобы модули `config`, `database`, `handlers` корректно импортировались
при запуске `python -m app.main` или при деплое на хостинги, которые ожидают модуль `app`.
"""

import asyncio
import logging
import sys
from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

# Гарантируем, что корень проекта есть в sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from config import BOT_TOKEN  # noqa: E402
from database import init_db  # noqa: E402
from handlers import (  # noqa: E402
    start_router,
    menu_router,
    sessions_router,
    packages_router,
    designs_router,
    custom_style_router,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    if not BOT_TOKEN:
        logger.error("Укажи BOT_TOKEN в .env")
        return
    await init_db()
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.include_router(start_router)
    dp.include_router(menu_router)
    dp.include_router(sessions_router)
    dp.include_router(packages_router)
    dp.include_router(designs_router)
    dp.include_router(custom_style_router)
    await dp.start_polling(bot)


def run():
    asyncio.run(main())


if __name__ == "__main__":
    run()

