# i know you will use command on this file
import discord
from discord.ext import commands
from discord import app_commands

class SourceCode(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
    @app_commands.command(name='sourcecode', description='Shows source code of the command')
    async def sourcecode(self, interaction:discord.Interaction):
        ...