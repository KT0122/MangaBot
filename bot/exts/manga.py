import asyncio
import os

import discord
from discord import app_commands
from discord.ext import commands

from bot.utils.pagination import Pagination
from bot.utils.MangaDexImplementation import mdAPI


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(mangaCommands(bot))


class mangaCommands(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.md = mdAPI()

    @app_commands.command(name="searchmdex", description="Search for Manga from MangaDex right from your discord")
    @app_commands.describe(title="Title of the mangga")
    async def SearchMDex(self, interaction: discord.Interaction, title: str) -> None:
        """ 
        Search MangaDex for a user specified manga and return to them an embedd containing a link and other info
        about the manga

        Args:
            interaction (discord.Interaction): Necessary for slash commands to function properly
            title (str): _description_
        """
        mangaJson = self.md.getMangaJson(title)

        if mangaJson is None:
            await interaction.response.send_message("Something went wrong. Here are some possible reasons:\n"  # noqa
                                                    "1. The manga youre looking for does not exist on MDex's site\n"
                                                    "2. Something about the spelling is wrong\n"
                                                    "3. Its MDex's fault\n"
                                                    "4. You searched for Pokemon\n")
        else:
            embeds = self.md.createDiscordEmbed(mangaJson=mangaJson)

            async def getPage(page: int):
                embed = embeds[page]

                return embed, len(embeds)

            await Pagination(interaction=interaction, getPage=getPage).navigate()

    # At some point itll probably be a good idea to make a helper method to handle most of whats going on here
    # I'll come back to it later
    @app_commands.command(name="randomanga", description="Get a Random Manga from MangaDex, never know whats out there")
    async def RandomManga(self, interaction: discord.Interaction) -> None:
        """
        Search for a random manga from MangaDex and return it to the user
        
        Args:
            interaction (discord.Interaction): Necessary for slash commands to function properly
        """
        
        mangaJson = self.md.getRandomManga()
        embeds = self.md.createDiscordEmbed(mangaJson=mangaJson)

        # Preemptive measures to avoid unkown interaction errors
        await interaction.response.defer()  # noqa
        await asyncio.sleep(2)

        async def getPage(page: int):
            embed = embeds[page]

            return embed, len(embeds)

        await Pagination(interaction=interaction, getPage=getPage).navigate()

    @app_commands.command(name="mangastats", description="Retrieve the statistics of a chosen manga")
    async def MangaStats(self, interation: discord.Interaction) -> None:

        await interation.response.defer()

    # if this is still here in 2024 someone bother me to fix it
    @app_commands.command(name="pokemon", description="If you're wondering why you cant search Pokemon Manga")
    async def WhyWereNotAllowedToSearchForPokemonRN(self, interaction: discord.Interaction) -> None:
        """
        Just an explanation as to why Pokemon searches are currently being filtered out, idk why Im writing this
        docstring tbh

        Args:
            interaction (discord.Interaction): Necessary for slash commands to function properly
        """
        
        await interaction.response.send_message("If you're here you're probably wondering \"Why cant we lookup "  # noqa
                                                "Pokemon?\"\nPokemon searches on MDex's API seem to be somewhat "
                                                "broken. Using the API to search up Pokemon will bring up various "
                                                "Pokemon spinoffs, not the original series. Meanhwile searching on "
                                                "MDex's site will bring up the original Pokemon but none of those "
                                                "spinoffs. Because of this all Pokemon searches are disabled until a "
                                                "proper fix can be implemented. If this still isnt fixxed in 2024 find"
                                                " someone who knows and will bother my creator about it.")
        