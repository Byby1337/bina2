from aiogram import Router
from aiogram.types import CallbackQuery
from keyboards import back_to_main_kb

router = Router()


@router.callback_query(lambda c: c.data and c.data.startswith("session:"))
async def choose_session(callback: CallbackQuery):
    num = callback.data.split(":")[1]
    await callback.message.edit_text(
        f"Выбрано: <b>{num} сессий</b>. Теперь выбери пакет сигналов в главном меню.",
        reply_markup=back_to_main_kb(),
    )
    await callback.answer(f"Сессий: {num}")
