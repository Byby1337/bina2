import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
CURRENCY = os.getenv("CURRENCY", "USD")

# Если api.openai.com недоступен (блокировка, регион) — укажи зеркало или прокси:
OPENAI_API_BASE_URL = os.getenv("OPENAI_API_BASE_URL", "").strip() or None
OPENAI_API_TIMEOUT = int(os.getenv("OPENAI_API_TIMEOUT", "60"))
# Прокси для запросов к OpenAI. Допустимые форматы:
# http://host:port   или   http://user:pass@host:port
# или коротко: user:pass:host:port  (будет преобразовано в http://user:pass@host:port)
_raw_proxy = os.getenv("OPENAI_PROXY", "").strip() or None
if _raw_proxy and not _raw_proxy.startswith(("http://", "https://", "socks4://", "socks5://")):
    parts = _raw_proxy.split(":")
    if len(parts) == 4:
        _raw_proxy = f"http://{parts[0]}:{parts[1]}@{parts[2]}:{parts[3]}"
    elif len(parts) == 2:
        _raw_proxy = f"http://{_raw_proxy}"
OPENAI_PROXY = _raw_proxy or None

# Crypto Pay (CryptoBot) — токен из @CryptoBot → Crypto Pay → Create App
CRYPTO_PAY_API_TOKEN = os.getenv("CRYPTO_PAY_API_TOKEN", "")
# Тестовая сеть: https://testnet-pay.crypt.bot
CRYPTO_PAY_TESTNET = os.getenv("CRYPTO_PAY_TESTNET", "").lower() in ("1", "true", "yes")
CRYPTO_PAY_BASE_URL = "https://testnet-pay.crypt.bot/api" if CRYPTO_PAY_TESTNET else "https://pay.crypt.bot/api"

# Пакеты сигналов: название -> (количество сигналов, цена в USD)
SIGNAL_PACKAGES = {
    "small": ("10 сигналов", 15),
    "medium": ("30 сигналов", 35),
    "large": ("50 сигналов", 50),
    "mega": ("100 сигналов", 85),
}

# Варианты количества сессий
SESSION_OPTIONS = [1, 3, 5, 10, 20]

# ID дизайнов под биржи
DESIGN_IDS = {
    "binomo": "Binomo",
    "pocket_option": "Pocket Option",
    "quotex": "Quotex",
    "binarium": "Binarium",
}

DB_PATH = BASE_DIR / "bot_data.db"
