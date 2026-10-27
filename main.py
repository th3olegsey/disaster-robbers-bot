import discord
import os
import asyncio

from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
load_dotenv()
token = os.getenv('token')
cmds = ['calc','notifyStarfall', 'statCmds', 'scary', 'leaderboard']
bg_tasks = ['getDRservers']
events = ['logEveryCommand']
class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.guilds = True
        intents.members = True
        super().__init__(command_prefix='!', intents=intents)
    
    async def setup_hook(self):
        for cmd in cmds:
            await self.load_extension(f'Commands.{cmd}')
        for bg_task in bg_tasks:
            await self.load_extension(f'BG_Tasks.{bg_task}')
        for event in events:
            await self.load_extension(f'Events.{event}')

        guild = os.getenv('guild')
        if guild and guild.isdigit():
            guild = discord.Object(int(guild))
            self.tree.copy_global_to(guild=guild)
            self.tree.clear_commands(guild=None)
            await self.tree.sync(guild=guild)
            print('cmds have been synced to specific guild')
        else:
            await self.tree.sync()
            print('cmds have been synced globally')

    async def on_ready(self):
        print('im ready')
if not token:
    raise SystemExit('Set discord token')
bot = Bot()

@bot.tree.command(name='reload_commands')
async def reloadCommands(interaction:discord.Interaction):
    for cmd in cmds:
        await bot.unload_extension(f'Commands.{cmd}')
    for bg_task in bg_tasks:
        await bot.unload_extension(f'BG_Tasks.{bg_task}')
    for event in events:
        await bot.unload_extension(f'Events.{event}')

    try:
        for cmd in cmds:
            await bot.load_extension(f'Commands.{cmd}')
        for bg_task in bg_tasks:
            await bot.load_extension(f'BG_Tasks.{bg_task}')
        for event in events:
            await bot.load_extension(f'Events.{event}')
        await interaction.response.send_message('reloaded', ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f'Failed: {e}')
bot.run(token)
