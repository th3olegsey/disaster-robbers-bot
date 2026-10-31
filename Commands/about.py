import discord
from discord.ext import commands
from discord import app_commands



class About(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @app_commands.command(name='about', description='Shows information about this bot')
    async def about(self, interaction:discord.Interaction):
        app_info = await self.bot.application_info()
        developer = app_info.owner.mention
        embed = discord.Embed(title=f'About {app_info.name} ({app_info.id})', description=f'This bot was made by {developer}')
        supportedCommands = ''
        for command in self.bot.cmds:
            supportedCommands = f'{supportedCommands}{command.mention}: {command.description}\n'
        embed.add_field(name='Supported commands', value=supportedCommands)
        await interaction.response.send_message(embed=embed)
async def setup(bot:commands.Bot):
    await bot.add_cog(About(bot))