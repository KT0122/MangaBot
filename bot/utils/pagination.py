import discord
from typing import Callable, Optional



class Pagination(discord.ui.View):
    
    def __init__(self, interaction: discord.Interaction, getPage: callable):
        self.interaction = interaction
        self.getPage = getPage
        self.totalPages = 0
        self.index = 0
        super().__init__(timeout=100)

    async def interactionCheck(self, interaction: discord.Interaction) -> bool:
        if interaction.user == self.interaction.user:
            return True
        else:
            embed = discord.Embed(
                description=f"Only the caller can preform this action",
                color=16711680
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return False
        
    async def navigate(self) -> None:
        embed, self.totalPages = await self.getPage(self.index)

        # I didnt really want to do this like this, but that weird bug with
        # set_image is coming back to bite me gdi
        if self.totalPages == 1:
            await self.interaction.response.send_message(embed=embed, view=self)

        elif self.totalPages > 1:
            self.updateButtons()
            await self.interaction.response.send_message(embed=embed, view=self)
     
    async def editPages(self, interaction: discord.Interaction) -> None:
        embed, self.totalPages = await self.getPage(self.index)
        await self.updateButtons()

        await interaction.response.edit_message(embed=embed, view=self)

    async def updateButtons(self) -> None:
        if self.index > self.totalPages // 2:
            self.children[2].emoji = "⏮️"
        else:
            self.children[2].emoji = "⏭️"
        
        self.children[0].disabled = self.index == 1
        self.children[1].disabled = self.index == self.totalPages
    
    @discord.ui.button(emoji="◀️", style=discord.ButtonStyle.secondary)
    async def previous(self, interaction: discord.Interaction, button: discord.Button):
        self.index -= 1
        await self.editPages(interaction=interaction)
    
    @discord.ui.button(emoji="▶️", style=discord.ButtonStyle.secondary)
    async def next(self, interaction: discord.Interaction, button: discord.Button):
        self.index += 1
        await self.editPages(interaction=interaction)
    
    @discord.ui.button(emoji="⏭️", style=discord.ButtonStyle.secondary)
    async def end(self, interaction: discord.Interaction, button: discord.Button):
        if self.index <= self.totalPages // 2:
            self.index = self.totalPages
        else:
            self.index = 1
        await self.editPages(interaction=interaction)
    
    async def onTimeout(self) -> None:
        message = await self.interaction.original_response()
        await message.edit(view=None)
