import discord
from discord import app_commands
from discord.ext import commands

""" Ive been hit with a huge amount of inspiration about 2 mins before creating this class so here we go """


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(react(bot))


class react(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.ctx_menu = app_commands.ContextMenu(
            name="Grass",
            callback=self.shanks,
        )
        self.bot.tree.add_command(self.ctx_menu)

    @app_commands.describe()
    async def shanks(self, interaction: discord.Interaction,  message: discord.Message) -> None:
        await interaction.response.defer(ephemeral=True) # noqa
        await interaction.followup.send("Reaction Sent")
        await message.reply("https://i.imgur.com/19G5u0Q.jpg")
        pass
