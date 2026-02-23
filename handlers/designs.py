from aiogram import Router
from aiogram.types import CallbackQuery
from config import DESIGN_IDS
from keyboards import back_to_main_kb
from templates.designs import format_signal

router = Router()


@router.callback_query(lambda c: c.data and c.data.startswith("design:"))
async def choose_design(callback: CallbackQuery):
    design_id = callback.data.split(":")[1]
    if design_id not in DESIGN_IDS:
        await callback.answer("Неизвестный дизайн")
        return
    name = DESIGN_IDS[design_id]
    # Показываем пример сигнала в этом дизайне
    example = format_signal(design_id, "EUR/USD", "CALL", "M5", "Не инвестируйте больше, чем готовы потерять.")
    await callback.message.edit_text(
        f"Дизайн: <b>{name}</b>\n\nПример сигнала в этом стиле:\n\n{example}",
        reply_markup=back_to_main_kb(),
    )
    await callback.answer(name)
