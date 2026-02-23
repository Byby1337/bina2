# Шаблоны оформления сигналов под разные бинарные платформы.
# Каждый шаблон — функция, возвращающая текст поста сигнала по данным (пара, направление, таймфрейм и т.д.).

DESIGN_NAMES = {
    "binomo": "Binomo",
    "pocket_option": "Pocket Option",
    "quotex": "Quotex",
    "binarium": "Binarium",
}


def _binomo_signal(asset: str, direction: str, timeframe: str, note: str = "") -> str:
    direction_emoji = "🟢" if direction.lower() in ("call", "вверх", "buy") else "🔴"
    return (
        f"📊 <b>BINOMO — Сигнал</b>\n\n"
        f"🪙 Актив: <b>{asset}</b>\n"
        f"{direction_emoji} Направление: <b>{direction}</b>\n"
        f"⏱ Свеча: <b>{timeframe}</b>\n\n"
        f"📌 Только по тренду. Управляйте риском.\n"
        f"{note}"
    ).strip()


def _pocket_option_signal(asset: str, direction: str, timeframe: str, note: str = "") -> str:
    direction_emoji = "⬆️" if direction.lower() in ("call", "вверх", "buy") else "⬇️"
    return (
        f"⚡ <b>POCKET OPTION</b> | Сигнал\n"
        f"────────────────\n"
        f"• Актив: {asset}\n"
        f"• Сделка: {direction_emoji} {direction}\n"
        f"• Таймфрейм: {timeframe}\n"
        f"────────────────\n"
        f"{note}\n"
        f"#PocketOption #Signals"
    ).strip()


def _quotex_signal(asset: str, direction: str, timeframe: str, note: str = "") -> str:
    direction_emoji = "📈" if direction.lower() in ("call", "вверх", "buy") else "📉"
    return (
        f"🔥 Quotex — Сигнал\n\n"
        f"Актив: {asset} | {timeframe}\n"
        f"Направление: {direction_emoji} {direction}\n\n"
        f"⚠️ Риск-менеджмент обязателен.\n"
        f"{note}"
    ).strip()


def _binarium_signal(asset: str, direction: str, timeframe: str, note: str = "") -> str:
    direction_emoji = "✅ CALL" if direction.lower() in ("call", "вверх", "buy") else "❌ PUT"
    return (
        f"📌 Бинариум | Сигнал\n"
        f"━━━━━━━━━━━━━━\n"
        f"Актив: <b>{asset}</b>\n"
        f"Тип: {direction_emoji}\n"
        f"Свеча: {timeframe}\n"
        f"━━━━━━━━━━━━━━\n"
        f"{note}"
    ).strip()


_TEMPLATES = {
    "binomo": _binomo_signal,
    "pocket_option": _pocket_option_signal,
    "quotex": _quotex_signal,
    "binarium": _binarium_signal,
}


def get_signal_template(design_id: str):
    return _TEMPLATES.get(design_id, _binomo_signal)


def format_signal(design_id: str, asset: str, direction: str, timeframe: str, note: str = "") -> str:
    fn = get_signal_template(design_id)
    return fn(asset, direction, timeframe, note)
