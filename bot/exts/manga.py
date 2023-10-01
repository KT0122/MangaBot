import os

import discord
from discord import app_commands
from discord.ext import commands

from bot.utils.MangaDexImplementation import mdAPI


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(mangaCommands(bot))


class mangaCommands(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.md = mdAPI()

    # @commands.command(name="SearchMDex")
    @app_commands.command(name="searchmdex")
    @app_commands.describe(title="Title of the mangga")
    async def SearchMDex(self, interaction: discord.Interaction, title: str) -> None:
        """
        Search manga dex for a user specified manga and return to them an embedd containing a link and other info
        about the manga

        :param interaction: Necessary for slash commands to function properly
        :param title: Title of the manga to be searched for, passed in by user
        """
        # md = mdAPI()
        mangaJson = self.md.getMangaJson(title)

        path = self.md.getMangaCover(mangaJson=mangaJson)
        embed = self.md.createDiscordEmbed(mangaJson=mangaJson)

        # There's a strange bug on library end where the image isnt being set with the actual url retrieved from the
        # MangaDex API for now iamages are created and sent alongside the embed before having their files closed and
        # deleted by the OS
        file = discord.File(path, filename="cover.jpg")
        embed.set_image(url="attachment://cover.jpg")

        # Pycharm marks this as an unresolved reference but it both shows up in the API documentation and works so
        await interaction.response.send_message(embed=embed, file=file)  # noqa
        file.close()
        os.remove(path)

    # At some point itll probably be a good idea to make a helper method to handle most of whats going on here
    # I'll come back to it later
    @app_commands.command(name="randomanga")
    async def RandomManga(self, interaction: discord.Interaction):
        mangaJson = self.md.getRandomManga()

        path = self.md.getMangaCover(mangaJson=mangaJson)
        embed = self.md.createDiscordEmbed(mangaJson=mangaJson)

        # deleted by the OS
        file = discord.File(path, filename="cover.jpg")
        embed.set_image(url="attachment://cover.jpg")

        await interaction.response.send_message(embed=embed, file=file)  # noqa
        file.close()
        os.remove(path)
