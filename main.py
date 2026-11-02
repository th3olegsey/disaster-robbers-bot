import discord

from discord.ext import commands
from discord import app_commands
from os import getenv
from dotenv import load_dotenv
load_dotenv()
token = getenv('token')
cmds = ['calc', 'notifyStarfall', 'statCmds', 'scary', 'leaderboard', 'lbActions', 'about']
bg_tasks = ['getDRservers', 'updateLeaderboardNames']
events = ['logEveryCommand']

class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.guilds = True
        intents.members = True
        intents.message_content = True
        super().__init__(command_prefix='!', intents=intents)
        self.cmds = []
    
    async def setup_hook(self):
        for cmd in cmds:
            await self.load_extension(f'Commands.{cmd}')
        for bg_task in bg_tasks:
            await self.load_extension(f'BG_Tasks.{bg_task}')
        for event in events:
            await self.load_extension(f'Events.{event}')

        guild = discord.Object(1494094131692048578)
        #self.tree.copy_global_to(guild=guild)
        #self.tree.clear_commands(guild=None)
        bot_cmds = await self.tree.sync()
        for command in bot_cmds:
            self.cmds.append(command)
        print('cmds have been synced')

    async def on_ready(self):
        print('im ready')
if not token:
    raise SystemExit('Set discord token')
bot = Bot()

bot.run(token)
