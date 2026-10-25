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
        await self.load_extension('Commands.calc')
        await self.load_extension('Commands.notifyStarfall')
        await self.load_extension('Commands.statCmds')
        await self.load_extension('BG_Tasks.getDRservers')
        await self.load_extension('Commands.scary')

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
