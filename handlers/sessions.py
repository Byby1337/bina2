from aiogram import Router
from aiogram.types import CallbackQuery
from config import SESSION_SURCHARGE
from keyboards import back_to_main_kb

router = Router()


@router.callback_query(lambda c: c.data and c.data.startswith("session:"))
async def choose_session(callback: CallbackQuery):
    num_str = callback.data.split(":")[1]
    try:
        num = int(num_str)
    except ValueError:
        await callback.answer("Ошибка выбора сессий", show_alert=True)
        return
    extra = SESSION_SURCHARGE.get(num, 0)
    base_text = "сессия" if num == 1 else "сессии"
    extra_text = (
        f"К базовой цене подписки будет добавлено +${extra}."
        if extra > 0
        else "Без доплаты к базовой цене подписки."
    )
    await callback.message.edit_text(
        f"Выбрано: <b>{num} {base_text} в день</b>.\n\n{extra_text}\n\n"
        "Теперь выбери тариф подписки в главном меню.",
        reply_markup=back_to_main_kb(),
    )
    await callback.answer(f"Сессий в день: {num}")
