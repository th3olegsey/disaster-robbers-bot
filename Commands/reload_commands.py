import discord
from discord.ext import commands
from discord import app_commands
from main import cmds, bg_tasks, events

class Reload_commands(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @app_commands.command(name='reload_commands', description='Updates all commands')
    async def reloadCommands(self, interaction:discord.Interaction):
        for cmd in cmds:
            await self.bot.unload_extension(f'Commands.{cmd}')
            try:
                await self.bot.load_extension(f'Commands.{cmd}')
            except Exception as e:
                print(f'Failed to load extension {cmd}: {e}')

        for bg_task in bg_tasks:
            await self.bot.unload_extension(f'BG_Tasks.{bg_task}')
            try:
                await self.bot.load_extension(f'BG_Tasks.{bg_task}')
            except Exception as e:
                print(f'Failed to load extension {bg_task}: {e}')

        for event in events:
            await self.bot.unload_extension(f'Events.{event}')
            try:
                await self.bot.load_extension(f'Events.{event}')
            except Exception as e:
                print(f'Failed to load extension {event}: {e}')

        await interaction.response.send_message('reloaded', ephemeral=True)
async def setup(bot:commands.Bot):
    await bot.add_cog(Reload_commands(bot))