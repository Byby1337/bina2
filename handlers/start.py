from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from keyboards import main_menu_kb
from database import get_or_create_user

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    user = message.from_user
    if user:
        await get_or_create_user(user.id, user.username, user.first_name)
    await message.answer(
        "Привет! Я бот для аффилиат-проектов: помогаю получать пакеты сигналов "
        "без живых сигнальщиков.\n\n"
        "• Выбери количество сессий\n"
        "• Пакет сигналов по цене\n"
        "• Дизайн под Binomo, Pocket Option, Quotex или Binarium\n"
        "• Либо загрузи пример поста — и я буду делать сигналы в твоём стиле с помощью AI\n\n"
        "Выбери действие:",
        reply_markup=main_menu_kb(),
    )
