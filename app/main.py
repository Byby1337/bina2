"""
Entry point для запуска бота как модуля `app`.

Поддерживаем оба сценария:
- python -m app.main
- импорт main()/run() из app.main (некоторые хостинги так стартуют процесс)
"""

import asyncio

# Импортируем существующий запуск из корневого main.py
from main import main as _root_main


async def main():
    await _root_main()


def run():
    asyncio.run(main())


if __name__ == "__main__":
    run()

