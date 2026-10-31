import discord
import os
from discord import app_commands
from discord.ext import commands
from Data.Guild.Users.User import get_stat, set_stat
stats = []
choises = []
files = os.listdir('Data/Guild/Users')
for file in files:
    if file.endswith('.csv'):
        stats.append(file[0:-4])

for stat in stats:
    choises.append(app_commands.Choice(name=stat, value=stat))
embed = discord.Embed(title='Access denied', description='You are no supposed to use this command', color=0xFF0000)
class StatCmds(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @app_commands.choices(stat=choises)
    @app_commands.command(name='getstat', description='Gets users stat')
    async def getrep(self, interaction:discord.Interaction, user:discord.User, stat:app_commands.Choice[str]):
        if interaction.user.id != 884134020693229639:
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        userid = user.id
        await interaction.response.send_message(f'{user.name}: {get_stat(userid, stat.value)}', ephemeral=True)

    @app_commands.choices(stat=choises)
    @app_commands.command(name='setstat', description='Sets users stat')
    async def setrep(self, interaction:discord.Interaction, user:discord.User, stat:app_commands.Choice[str], value:int):
        if interaction.user.id != 884134020693229639:
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        userid = user.id
        old_rep = get_stat(userid, stat.value)
        new_rep = value
        set_stat(userid, stat.value, value)
        await interaction.response.send_message(f'{user.name}: {old_rep} -> {new_rep}', ephemeral=True)

async def setup(bot:commands.Bot):
    await bot.add_cog(StatCmds(bot))