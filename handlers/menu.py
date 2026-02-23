from aiogram import Router
from aiogram.types import CallbackQuery
from keyboards import main_menu_kb, sessions_kb, packages_kb, designs_kb, custom_style_upload_kb
from database import get_user_custom_styles

router = Router()


@router.callback_query(lambda c: c.data == "menu:main")
async def back_to_main(callback: CallbackQuery):
    await callback.message.edit_text(
        "Главное меню. Выбери раздел:",
        reply_markup=main_menu_kb(),
    )
    await callback.answer()


@router.callback_query(lambda c: c.data == "menu:sessions")
async def show_sessions(callback: CallbackQuery):
    await callback.message.edit_text(
        "Выбери количество сессий (сколько раз в день/неделю будут выдаваться сигналы):",
        reply_markup=sessions_kb(),
    )
    await callback.answer()


@router.callback_query(lambda c: c.data == "menu:packages")
async def show_packages(callback: CallbackQuery):
    await callback.message.edit_text(
        "Пакеты сигналов. Цена зависит от количества:",
        reply_markup=packages_kb(),
    )
    await callback.answer()


@router.callback_query(lambda c: c.data == "menu:designs")
async def show_designs(callback: CallbackQuery):
    await callback.message.edit_text(
        "Выбери дизайн под платформу. Сигналы будут оформлены в стиле выбранной биржи:",
        reply_markup=designs_kb(),
    )
    await callback.answer()


@router.callback_query(lambda c: c.data == "menu:custom_style")
async def show_custom_style(callback: CallbackQuery):
    styles = await get_user_custom_styles(callback.from_user.id) if callback.from_user else []
    await callback.message.edit_text(
        "Свой стиль (AI):\n\n"
        "Отправь сюда пример поста из своего или чужого канала. "
        "Бот проанализирует оформление и будет генерировать дальнейшие сигналы в этом же стиле.",
        reply_markup=custom_style_upload_kb(has_styles=len(styles) > 0),
    )
    await callback.answer()
