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
##############################
########### Events ###########
##############################
@bot.event
async def on_interaction(interaction: discord.Interaction):
    log_channel = await bot.fetch_channel(1495456107081105470)
    if interaction.command != None and interaction.type == discord.InteractionType.application_command:
        esc = chr(27)
        if interaction.data.__contains__('options'):
            params = ''
            for i in interaction.data['options']:
                params = f'{params}{i['value']} '
            await log_channel.send(f'```ansi\n{esc}[1;34m{interaction.user}{esc}[0m: {esc}[1;31m{interaction.data["name"]}{esc}[0m {esc}[1;33m{params}{esc}[0m```')
        else:
            await log_channel.send(f'```ansi\n{esc}[1;34m{interaction.user}{esc}[0m: {esc}[1;31m{interaction.data["name"]}{esc}[0m```')

bot.run(token)
