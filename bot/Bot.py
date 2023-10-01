# Built in
import logging
import discord

from discord.ext import commands


class MangaBot(commands.Bot):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def sync_app_commands(self) -> None:
        await self.tree.sync()
        print("Command tree synced")

        logging.info("Command tree synced")

    async def setup_hook(self) -> None:
        cog = "exts.manga"
        await self.load_extension(cog)
        await self.sync_app_commands()
