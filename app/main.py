import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config import BOT_TOKEN
from database import init_db
from handlers import (
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


if __name__ == "__main__":
    asyncio.run(main())
