from discord.ext import commands


class MangaBot(commands.Bot):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def setup_hook(self) -> None:
        cog = "exts.manga"
        await self.load_extension(cog)
