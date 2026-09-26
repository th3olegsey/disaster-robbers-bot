import discord
from discord import app_commands
from discord.ext import commands

class Btn(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(emoji=':ghost:')
    async def btnClick(self, interaction:discord.Interaction, button: discord.Button):
        await interaction.response.send_message('Scary :ghost:')

class Boo(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @app_commands.command(name='boo', description='scary')
    async def boo(self, interaction:discord.Interaction):
        await interaction.response.send_message('Scary', view=Btn())

async def setup(bot:commands.Bot):
    await bot.add_cog(Boo(bot))