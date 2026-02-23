from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import SESSION_OPTIONS, SIGNAL_PACKAGES, DESIGN_IDS


def main_menu_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="📦 Выбрать пакет сигналов", callback_data="menu:packages"),
        InlineKeyboardButton(text="🔄 Количество сессий", callback_data="menu:sessions"),
    )
    builder.row(
        InlineKeyboardButton(text="🎨 Дизайн под платформу", callback_data="menu:designs"),
        InlineKeyboardButton(text="✨ Свой стиль (AI)", callback_data="menu:custom_style"),
    )
    return builder.as_markup()


def sessions_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for n in SESSION_OPTIONS:
        builder.row(
            InlineKeyboardButton(text=f"{n} сессий", callback_data=f"session:{n}"),
        )
    builder.row(InlineKeyboardButton(text="◀️ В меню", callback_data="menu:main"))
    return builder.as_markup()


def packages_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for key, (label, price) in SIGNAL_PACKAGES.items():
        builder.row(
            InlineKeyboardButton(
                text=f"{label} — ${price}",
                callback_data=f"package:{key}",
            ),
        )
    builder.row(InlineKeyboardButton(text="◀️ В меню", callback_data="menu:main"))
    return builder.as_markup()


def designs_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for design_id, name in DESIGN_IDS.items():
        builder.row(
            InlineKeyboardButton(text=name, callback_data=f"design:{design_id}"),
        )
    builder.row(InlineKeyboardButton(text="◀️ В меню", callback_data="menu:main"))
    return builder.as_markup()


def pay_crypto_kb(invoice_url: str, invoice_id: int) -> InlineKeyboardMarkup:
    """Кнопка оплаты (ссылка на Crypto Bot) и проверка оплаты."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="💳 Оплатить через Crypto Bot", url=invoice_url),
    )
    builder.row(
        InlineKeyboardButton(text="✅ Проверить оплату", callback_data=f"pay_check:{invoice_id}"),
    )
    builder.row(InlineKeyboardButton(text="◀️ В меню", callback_data="menu:main"))
    return builder.as_markup()


def back_to_main_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="◀️ В меню", callback_data="menu:main"))
    return builder.as_markup()


def custom_style_upload_kb(has_styles: bool = False) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="📤 Загрузить пример поста", callback_data="custom_style:upload"),
    )
    if has_styles:
        builder.row(
            InlineKeyboardButton(text="🎲 Сгенерировать сигнал в моём стиле", callback_data="custom_style:generate"),
        )
    builder.row(InlineKeyboardButton(text="◀️ В меню", callback_data="menu:main"))
    return builder.as_markup()
