# External Imports
import asyncio
import discord
import logging
import logging.handlers

# Project Modules
from Bot import MangaBot
import BotConstants


async def main() -> None:
    logger = logging.getLogger('discord')
    logger.setLevel(logging.DEBUG)
    logging.getLogger('discord.http').setLevel(logging.INFO)

    handler = logging.handlers.RotatingFileHandler(
        filename='../discord.log',
        encoding='utf-8',
        maxBytes=32 * 1024 * 1024,  # 32 MiB
        backupCount=5,  # Rotate through 5 files
    )

    dt_fmt = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    intents = discord.Intents.default()
    intents.message_content = True

    client = MangaBot(intents=intents, command_prefix=BotConstants.prefix)
    await client.start(BotConstants.token)


if __name__ == "__main__":
    asyncio.run(main())
