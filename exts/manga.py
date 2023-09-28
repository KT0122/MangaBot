import os
import discord
from discord.ext import commands

from utils.MangaDexImplementation import mdAPI


def createMangaEmbed(mangaJson, md) -> [discord.Embed, discord.File, str]:
    path = md.getMangaCover(mangaJson=mangaJson)
    embed = md.createDiscordEmbed(mangaJson=mangaJson)

    file = discord.File(path, filename="cover.jpg")
    embed.set_image(url="attachment://cover.jpg")

    return embed, file, path


async def setup(bot: commands.Bot) -> None:
    """Sets up the cog"""

    await bot.add_cog(mangaCommands(bot))


class mangaCommands(commands.Cog):
    @commands.command(name="SearchMDex")
    async def SearchMDex(self, ctx, *, message):
        """
        Search manga dex for a user specified manga and return to them an embedd containing a link and other info
        about the manga

        :param ctx:
        :param message: The message from the user after the command call
        """
        md = mdAPI()
        mangaJson = md.getMangaJson(message)

        print(mangaJson)

        path = md.getMangaCover(mangaJson=mangaJson)
        embed = md.createDiscordEmbed(mangaJson=mangaJson)

        file = discord.File(path, filename="cover.jpg")
        embed.set_image(url="attachment://cover.jpg")

        await ctx.send(embed=embed, file=file)
        os.remove(path)

    @commands.command()
    async def RandomManga(self, ctx):
        md = mdAPI()
        mangaJson = md.getRandomManga()
        embed, file, path = createMangaEmbed(mangaJson, md)

        await ctx.send(embed=embed, file=file)
        os.remove(path)

    @commands.command()
    async def testCog(self, ctx):
        await ctx.send("test cog")
