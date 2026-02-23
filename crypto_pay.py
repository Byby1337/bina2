"""
Клиент Crypto Pay API (CryptoBot) для создания инвойсов и проверки оплаты.
Документация: https://help.crypt.bot/crypto-pay-api
"""
import aiohttp
from config import CRYPTO_PAY_API_TOKEN, CRYPTO_PAY_BASE_URL

HEADERS = {"Crypto-Pay-API-Token": CRYPTO_PAY_API_TOKEN}


async def create_invoice(
    amount: float,
    description: str,
    payload: str,
    *,
    fiat: str = "USD",
    expires_in: int = 3600,
) -> dict | None:
    """
    Создать инвойс на сумму в фиате (USD).
    amount — сумма в USD (например 15.0).
    payload — строка до 4 КБ (например user_id:package_key для идентификации после оплаты).
    Возвращает объект Invoice с bot_invoice_url, invoice_id или None при ошибке.
    """
    if not CRYPTO_PAY_API_TOKEN:
        return None
    url = f"{CRYPTO_PAY_BASE_URL}/createInvoice"
    body = {
        "amount": str(amount),
        "currency_type": "fiat",
        "fiat": fiat,
        "description": description[:1024],
        "payload": payload[:4096],
        "expires_in": min(max(1, expires_in), 2678400),
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=body, headers=HEADERS) as resp:
            data = await resp.json()
            if data.get("ok") and "result" in data:
                return data["result"]
            return None


async def get_invoices(invoice_ids: str) -> list[dict]:
    """
    Получить инвойсы по списку ID (через запятую).
    Возвращает список объектов Invoice (поля status, invoice_id и т.д.).
    """
    if not CRYPTO_PAY_API_TOKEN:
        return []
    url = f"{CRYPTO_PAY_BASE_URL}/getInvoices"
    params = {"invoice_ids": invoice_ids}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, headers=HEADERS) as resp:
            data = await resp.json()
            if data.get("ok") and "result" in data:
                r = data["result"]
                return r if isinstance(r, list) else (r.get("items", []) if isinstance(r, dict) else [])
            return []


async def get_me() -> dict | None:
    """Проверка токена и получение информации о приложении."""
    if not CRYPTO_PAY_API_TOKEN:
        return None
    url = f"{CRYPTO_PAY_BASE_URL}/getMe"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=HEADERS) as resp:
            data = await resp.json()
            if data.get("ok"):
                return data.get("result")
            return None
