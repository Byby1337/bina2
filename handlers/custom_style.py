from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards import back_to_main_kb
from database import save_custom_style, get_user_custom_styles
from ai_service import extract_style_from_example, generate_signal_in_style

router = Router()

# Подсказка при ошибке соединения (блокировка api.openai.com)
def _openai_error_msg(e: Exception) -> str:
    err = str(e).strip() or type(e).__name__
    if "Connection" in type(e).__name__ or "connection" in err.lower() or "connect" in err.lower():
        return (
            f"Нет связи с API OpenAI ({err}).\n\n"
            "Часто так бывает из-за блокировки в регионе. В .env добавь зеркало:\n"
            "OPENAI_API_BASE_URL=https://твой-прокси-или-зеркало/v1\n\n"
            "Или используй VPN и перезапусти бота."
        )
    return f"Ошибка: {err}. Проверь OPENAI_API_KEY в .env."


class CustomStyleStates(StatesGroup):
    waiting_example = State()


@router.callback_query(lambda c: c.data == "custom_style:upload")
async def ask_for_example(callback: CallbackQuery, state: FSMContext):
    await state.set_state(CustomStyleStates.waiting_example)
    await callback.message.edit_text(
        "Отправь одним сообщением пример поста-сигнала из канала (текст или скрин с подписью). "
        "Бот сохранит стиль и будет генерировать новые сигналы в таком же оформлении.\n\n"
        "Для отмены отправь /cancel.",
        reply_markup=back_to_main_kb(),
    )
    await callback.answer()


async def _process_example(message: Message, state: FSMContext, text: str):
    await message.answer("Анализирую стиль...")
    try:
        style_description = await extract_style_from_example(text)
        user_id = message.from_user.id if message.from_user else 0
        style_id = await save_custom_style(user_id, text, style_description)
        await state.clear()
        await message.answer(
            f"Стиль сохранён (ID: {style_id}). Описание:\n\n{style_description}\n\n"
            "Теперь в разделе «Свой стиль» появится кнопка «Сгенерировать сигнал в моём стиле».",
            reply_markup=back_to_main_kb(),
        )
    except Exception as e:
        await message.answer("Ошибка при анализе. " + _openai_error_msg(e))


@router.message(CustomStyleStates.waiting_example, F.text)
async def receive_example_text(message: Message, state: FSMContext):
    text = (message.text or "").strip()
    if len(text) < 20:
        await message.answer("Слишком короткий текст. Отправь полный пример поста.")
        return
    await _process_example(message, state, text)


@router.message(CustomStyleStates.waiting_example, F.caption)
async def receive_example_caption(message: Message, state: FSMContext):
    text = (message.caption or "").strip()
    if len(text) < 20:
        await message.answer("Добавь подпись к фото/документу с примером поста или отправь текст.")
        return
    await _process_example(message, state, text)


@router.callback_query(lambda c: c.data == "custom_style:generate")
async def generate_in_style(callback: CallbackQuery):
    styles = await get_user_custom_styles(callback.from_user.id) if callback.from_user else []
    if not styles:
        await callback.answer("Сначала загрузи пример поста в разделе «Свой стиль».", show_alert=True)
        return
    style = styles[0]
    await callback.answer("Генерирую сигнал...")
    try:
        text = await generate_signal_in_style(style["style_description"], style["example_text"])
        await callback.message.answer(text)
    except Exception as e:
        await callback.message.answer("Ошибка генерации. " + _openai_error_msg(e))


@router.message(F.text, F.text.lower() == "/cancel")
async def cancel_custom_style(message: Message, state: FSMContext):
    if await state.get_state() == CustomStyleStates.waiting_example:
        await state.clear()
        await message.answer("Отменено.", reply_markup=back_to_main_kb())
    else:
        await message.answer("Нечего отменять.")
