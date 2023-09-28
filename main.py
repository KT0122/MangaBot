# External Imports
import asyncio
import discord

# Project Modules
from Bot import MangaBot
import BotConstants


async def main() -> None:
    intents = discord.Intents.default()
    intents.message_content = True

    client = MangaBot(intents=intents, command_prefix=BotConstants.prefix)
    await client.start(BotConstants.token)


if __name__ == "__main__":
    asyncio.run(main())
