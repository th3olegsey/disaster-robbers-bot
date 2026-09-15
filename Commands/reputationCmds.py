import discord
from discord import app_commands
from discord.ext import commands
from Data.Guild.Users.user import User

class ReputationCmds(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot


    @app_commands.command(name='getreputation', description='Gets users reputation')
    async def getrep(self, interaction:discord.Interaction, user:discord.User):
        userid = user.id
        userData = User(userid)
        await interaction.response.send_message(f'{userData.get_reputation()}')

    @app_commands.command(name='setreputation', description='Gets users reputation')
    async def setrep(self, interaction:discord.Interaction, user:discord.User, value:int):
        userid = user.id
        userData = User(userid)
        await interaction.response.send_message(f'{userData.set_reputation(value)}')

async def setup(bot:commands.Bot):
    await bot.add_cog(ReputationCmds(bot))