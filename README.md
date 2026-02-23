# Telegram-бот: сигналы для аффилиат-проектов (бинарные опционы)

Бот для аффилиат-проектов, которые льют трафик на бинарные платформы: выдаёт пакеты сигналов без живых сигнальщиков.

## Возможности

- **Количество сессий** — выбор числа сессий (1, 3, 5, 10, 20).
- **Пакеты сигналов** — разные объёмы по цене: 10 / 30 / 50 / 100 сигналов.
- **4 дизайна под платформы** — Binomo, Pocket Option, Quotex, Binarium (оформление поста под стиль каждой биржи).
- **Свой стиль (AI)** — пользователь отправляет пример поста из канала, бот через OpenAI анализирует стиль и дальше генерирует сигналы в этом же оформлении.
- **Оплата через Crypto Bot** — создание счёта в криптовалюте (Crypto Pay API), кнопка «Проверить оплату» после перевода.

## Установка и запуск

1. Клонируй или скопируй проект, перейди в папку:
   ```bash
   cd c:\Users\bubu\Desktop\project1
   ```

2. Создай виртуальное окружение и установи зависимости:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Создай бота в Telegram через [@BotFather](https://t.me/BotFather), получи токен.

4. Создай файл `.env` (скопируй из `.env.example`):
   ```env
   BOT_TOKEN=твой_токен_от_BotFather
   OPENAI_API_KEY=твой_ключ_OpenAI
   CURRENCY=USD
   CRYPTO_PAY_API_TOKEN=токен_из_CryptoBot
   ```
   Токен Crypto Pay: открой [@CryptoBot](https://t.me/CryptoBot) → Crypto Pay → Create App. Для тестов можно использовать [@CryptoTestnetBot](https://t.me/CryptoTestnetBot) и в .env добавить `CRYPTO_PAY_TESTNET=1`.

5. Запуск:
   ```bash
   python main.py
   ```

## Настройка

- **Пакеты и цены** — в `config.py` в `SIGNAL_PACKAGES`.
- **Варианты сессий** — в `config.py` в `SESSION_OPTIONS`.
- **Дизайны** — шаблоны в `templates/designs.py`, можно менять текст и эмодзи под каждую платформу.

## Структура проекта

```
project1/
├── main.py           # Точка входа, запуск бота
├── config.py         # Токены, пакеты, сессии, дизайны
├── crypto_pay.py     # Crypto Pay API: инвойсы и проверка оплаты
├── database.py       # SQLite: пользователи, заказы, кастомные стили
├── ai_service.py     # OpenAI: анализ стиля и генерация сигналов
├── requirements.txt
├── .env.example
├── keyboards/        # Inline-клавиатуры
├── handlers/         # Обработчики команд и callback
└── templates/        # Шаблоны оформления сигналов (4 платформы)
```

Для генерации в «своём стиле» нужен ключ OpenAI (например, для GPT-4o-mini). Без ключа раздел «Свой стиль (AI)» будет выдавать ошибку при загрузке примера и при генерации.
