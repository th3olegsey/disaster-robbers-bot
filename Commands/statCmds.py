import discord
from discord import app_commands
from discord.ext import commands
from Data.Guild.Users.user import get_stat, set_stat

class StatCmds(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot


    @app_commands.command(name='getstat', description='Gets users reputation')
    async def getrep(self, interaction:discord.Interaction, user:discord.User, stat:str):
        userid = user.id
        await interaction.response.send_message(f'{user.name}: {get_stat(userid, stat)}')

    @app_commands.command(name='setstat', description='Sets users reputation')
    async def setrep(self, interaction:discord.Interaction, user:discord.User, stat:str, value:int):
        if interaction.user.id != 884134020693229639:
            return await interaction.response.send_message('no', ephemeral=True)
        userid = user.id
        old_rep = get_stat(userid, stat)
        new_rep = value
        set_stat(userid, stat, value)
        await interaction.response.send_message(f'{user.name}: {old_rep} -> {new_rep}')

async def setup(bot:commands.Bot):
    await bot.add_cog(StatCmds(bot))