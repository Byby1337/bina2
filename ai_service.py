"""
Сервис для анализа примера поста и генерации сигналов в том же стиле через OpenAI.
При Connection error используй OPENAI_PROXY в .env (прокси) или OPENAI_API_BASE_URL (зеркало).
"""
from openai import AsyncOpenAI, DefaultAsyncHttpxClient
from config import OPENAI_API_KEY, OPENAI_API_BASE_URL, OPENAI_API_TIMEOUT, OPENAI_PROXY
import aiofiles
_client: AsyncOpenAI | None = None


def _get_client() -> AsyncOpenAI:
    global _client
    if _client is None:
        kwargs = {"api_key": OPENAI_API_KEY, "timeout": OPENAI_API_TIMEOUT}
        if OPENAI_API_BASE_URL:
            kwargs["base_url"] = OPENAI_API_BASE_URL.rstrip("/")
            if not kwargs["base_url"].endswith("/v1"):
                kwargs["base_url"] = kwargs["base_url"] + "/v1"
        if OPENAI_PROXY:
            kwargs["http_client"] = DefaultAsyncHttpxClient(
                proxy=OPENAI_PROXY,
                timeout=OPENAI_API_TIMEOUT,
            )
        _client = AsyncOpenAI(**kwargs)
    return _client


async def extract_style_from_example(example_text: str) -> str:
    """
    По тексту примера поста из канала описывает стиль (эмодзи, структура, формулировки).
    """
    client = _get_client()
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Ты эксперт по оформлению постов для каналов с сигналами для бинарных опционов. "
                "По примеру поста опиши кратко стиль: какие эмодзи используются, структура (заголовки, разделители), "
                "формулировки, тон. Ответь на русском, 3-5 предложений, без лишнего.",
            },
            {"role": "user", "content": example_text},
        ],
        max_tokens=300,
    )
    return (response.choices[0].message.content or "").strip()


async def generate_signal_in_style(style_description: str, example_text: str) -> str:
    """
    Генерирует один сигнал (актив, направление, таймфрейм) в описанном стиле,
    оформленный как пост для канала в том же формате, что и пример.
    """
    client = _get_client()
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Ты генерируешь посты-сигналы для канала бинарных опционов. "
                "Стиль и оформление должны строго совпадать с примером. "
                "Генерируй реалистичный сигнал: актив (например EUR/USD, GBP/JPY), направление (CALL или PUT), "
                "таймфрейм (например M1, M5). Вывод — только текст поста, без пояснений.",
            },
            {
                "role": "user",
                "content": f"Описание стиля:\n{style_description}\n\nПример поста:\n{example_text}\n\nСгенерируй один новый пост-сигнал в этом же стиле.",
            },
        ],
        max_tokens=400,
    )
    return (response.choices[0].message.content or "").strip()


async def generate_signal_with_template(design_id: str) -> tuple[str, str, str, str]:
    """
    Генерирует данные для сигнала (актив, направление, таймфрейм, заметка) через AI.
    Возвращает (asset, direction, timeframe, note).
    """
    client = _get_client()
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Ты выдаёшь один сигнал для бинарных опционов. Ответь строго в формате:\n"
                "ASSET: пара (например EUR/USD)\nDIRECTION: CALL или PUT\nTIMEFRAME: M1 или M5\nNOTE: короткая подсказка или пусто",
            },
            {"role": "user", "content": "Сгенерируй один случайный сигнал."},
        ],
        max_tokens=150,
    )
    text = (response.choices[0].message.content or "").strip()
    asset = "EUR/USD"
    direction = "CALL"
    timeframe = "M5"
    note = ""
    for line in text.split("\n"):
        line = line.strip()
        if line.upper().startswith("ASSET:"):
            asset = line.split(":", 1)[1].strip()
        elif line.upper().startswith("DIRECTION:"):
            direction = line.split(":", 1)[1].strip()
        elif line.upper().startswith("TIMEFRAME:"):
            timeframe = line.split(":", 1)[1].strip()
        elif line.upper().startswith("NOTE:"):
            note = line.split(":", 1)[1].strip()
    return asset, direction, timeframe, note


async def generate_image_from_style(
    client: AsyncOpenAI,
    style_image_path: str,  # путь к твоей картинке-стилю
    prompt_text: str        # текст, который нужно добавить
) -> str:
    """
    Генерирует картинку с текстом в стиле заданного изображения.
    Возвращает URL с результатом.
    """
    # читаем изображение в бинарном виде
    async with aiofiles.open(style_image_path, "rb") as f:
        style_image = await f.read()

    response = await client.images.edit(
        image=style_image,
        prompt=prompt_text,
        n=1,
        size="1024x1024",  # можно менять
    )

    return response.data[0].url