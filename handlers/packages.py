from aiogram import Router
from aiogram.types import CallbackQuery
from config import SIGNAL_PACKAGES, CRYPTO_PAY_API_TOKEN
from keyboards import back_to_main_kb, pay_crypto_kb
from crypto_pay import create_invoice, get_invoices
from database import create_order_with_invoice, get_order_by_invoice_id, set_order_paid

router = Router()


def _package_pay_kb(key: str):
    from aiogram.types import InlineKeyboardButton
    from aiogram.utils.keyboard import InlineKeyboardBuilder
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="💳 Оплатить через Crypto Bot", callback_data=f"pay:{key}"),
    )
    builder.row(InlineKeyboardButton(text="◀️ В меню", callback_data="menu:main"))
    return builder.as_markup()


@router.callback_query(lambda c: c.data and c.data.startswith("package:"))
async def choose_package(callback: CallbackQuery):
    key = callback.data.split(":")[1]
    if key not in SIGNAL_PACKAGES:
        await callback.answer("Неизвестный пакет")
        return
    label, price = SIGNAL_PACKAGES[key]
    text = (
        f"Пакет: <b>{label}</b> — ${price}. "
        "Оплата через Crypto Bot (криптовалюта)."
    )
    if not CRYPTO_PAY_API_TOKEN:
        text += "\n\n⚠️ Оплата не настроена: укажи CRYPTO_PAY_API_TOKEN в .env"
    await callback.message.edit_text(
        text,
        reply_markup=_package_pay_kb(key) if CRYPTO_PAY_API_TOKEN else back_to_main_kb(),
    )
    await callback.answer(f"{label} — ${price}")


@router.callback_query(lambda c: c.data and c.data.startswith("pay:"))
async def create_payment(callback: CallbackQuery):
    key = callback.data.split(":")[1]
    if key not in SIGNAL_PACKAGES:
        await callback.answer("Неизвестный пакет")
        return
    label, price = SIGNAL_PACKAGES[key]
    user = callback.from_user
    if not user:
        await callback.answer("Ошибка", show_alert=True)
        return
    await callback.answer("Создаём счёт...")
    payload = f"{user.id}:{key}"
    invoice = await create_invoice(
        amount=float(price),
        description=f"Пакет сигналов: {label}",
        payload=payload,
    )
    if not invoice:
        await callback.message.edit_text(
            "Не удалось создать счёт. Проверь CRYPTO_PAY_API_TOKEN в .env и настрой приложение в @CryptoBot.",
            reply_markup=back_to_main_kb(),
        )
        return
    invoice_id = invoice["invoice_id"]
    bot_invoice_url = invoice.get("bot_invoice_url") or invoice.get("pay_url", "")
    await create_order_with_invoice(user.id, key, float(price), invoice_id)
    await callback.message.edit_text(
        f"Оплати пакет <b>{label}</b> (${price}) по ссылке ниже. "
        "После оплаты нажми «Проверить оплату».",
        reply_markup=pay_crypto_kb(bot_invoice_url, invoice_id),
    )


@router.callback_query(lambda c: c.data and c.data.startswith("pay_check:"))
async def check_payment(callback: CallbackQuery):
    try:
        invoice_id = int(callback.data.split(":")[1])
    except (IndexError, ValueError):
        await callback.answer("Ошибка", show_alert=True)
        return
    order = await get_order_by_invoice_id(invoice_id)
    if not order:
        await callback.answer("Заказ не найден", show_alert=True)
        return
    if order["status"] == "paid":
        await callback.answer("Оплата уже зачислена.")
        await callback.message.edit_text(
            "✅ Этот заказ уже оплачен. Спасибо!",
            reply_markup=back_to_main_kb(),
        )
        return
    await callback.answer("Проверяю...")
    items = await get_invoices(str(invoice_id))
    if not items:
        await callback.answer("Платёж пока не найден. Оплати по ссылке и нажми снова.", show_alert=True)
        return
    inv = items[0]
    if inv.get("status") != "paid":
        await callback.answer("Оплата ещё не поступила. Попробуй через минуту.", show_alert=True)
        return
    await set_order_paid(order["id"])
    label, _ = SIGNAL_PACKAGES.get(order["package_key"], (order["package_key"], 0))
    await callback.message.edit_text(
        f"✅ Оплата получена! Пакет <b>{label}</b> активирован. Спасибо!",
        reply_markup=back_to_main_kb(),
    )
    await callback.answer("Оплата зачислена!")
