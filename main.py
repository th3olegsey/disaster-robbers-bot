import discord

from discord.ext import commands
from discord import app_commands
from os import getenv
from dotenv import load_dotenv
load_dotenv()
token = getenv('token')
cmds = ['calc','notifyStarfall', 'statCmds', 'scary', 'leaderboard', 'lbActions']
bg_tasks = ['getDRservers', 'updateLeaderboardNames']
events = ['logEveryCommand']

class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.guilds = True
        intents.members = True
        super().__init__(command_prefix='!', intents=intents)
        self.cmds = []
    
    async def setup_hook(self):
        for cmd in cmds:
            await self.load_extension(f'Commands.{cmd}')
        for bg_task in bg_tasks:
            await self.load_extension(f'BG_Tasks.{bg_task}')
        for event in events:
            await self.load_extension(f'Events.{event}')

        guild = getenv('guild')
        if guild and guild.isdigit():
            guild = discord.Object(int(guild))
            self.tree.copy_global_to(guild=guild)
            self.tree.clear_commands(guild=None)
            bot_cmds = await self.tree.sync(guild=guild)
            for command in bot_cmds:
                self.cmds.append(command)
            print('cmds have been synced to specific guild')
        else:
            bot_cmds = await self.tree.sync(guild=guild)
            for command in bot_cmds:
                self.cmds.append(command)
            print('cmds have been synced globally')

    async def on_ready(self):
        print('im ready')
if not token:
    raise SystemExit('Set discord token')
bot = Bot()
@bot.tree.command(name='reload_commands', description='Core command. Updates all commands')
async def reloadCommands(interaction:discord.Interaction):
    for cmd in cmds:
        await bot.unload_extension(f'Commands.{cmd}')
        try:
            await bot.load_extension(f'Commands.{cmd}')
        except Exception as e:
            print(f'Failed to load extension {cmd}: {e}')

    for bg_task in bg_tasks:
        await bot.unload_extension(f'BG_Tasks.{bg_task}')
        try:
            await bot.load_extension(f'BG_Tasks.{bg_task}')
        except Exception as e:
            print(f'Failed to load extension {bg_task}: {e}')

    for event in events:
        await bot.unload_extension(f'Events.{event}')
        try:
            await bot.load_extension(f'Events.{event}')
        except Exception as e:
            print(f'Failed to load extension {event}: {e}')

    await interaction.response.send_message('reloaded', ephemeral=True)

@bot.tree.command(name='about', description='Core command. Shows information about this bot')
async def about(interaction:discord.Interaction):
    app_info = await bot.application_info()
    developer = app_info.owner.mention
    embed = discord.Embed(title=f'About {app_info.name} ({app_info.id})', description=f'This bot was made by {developer}')
    supportedCommands = ''
    for command in bot.cmds:
        supportedCommands = f'{supportedCommands}{command.mention}: {command.description}\n'
    embed.add_field(name='Supported commands', value=supportedCommands)
    await interaction.response.send_message(embed=embed)

bot.run(token)
