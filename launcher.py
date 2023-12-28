import asyncio
import logging
import sys

from bot import MyBot
from config import token


async def main():
    # Redirect error to stderr
    logger = logging.getLogger('discord')
    logger.setLevel(logging.ERROR)
    handler = logging.StreamHandler(sys.stderr)
    logger.addHandler(handler)

    async with MyBot() as bot:
        await bot.start(token)


if __name__ == '__main__':
    asyncio.run(main())