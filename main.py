import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
load_dotenv()
token = os.getenv('token')
class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.guilds = True
        intents.members = True
        super().__init__(command_prefix='!', intents=intents)
    
    async def setup_hook(self):
        cmds = ['calc','notifyStarfall', 'statCmds', 'scary', 'leaderboard']
        bg_tasks = ['getDRservers']
        events = ['logEveryCommand']
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
bot.run(token)
