import discord
from discord import app_commands
from discord.ext import commands
import pandas as pd

class NotifyStarfall(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name='notifystarfall', description='Sends notification to the channel')
    async def notify(self, interaction:discord.Interaction, serverid: str):
        channel = interaction.channel
        servers = pd.read_csv('data/game/servers.csv')
        ids = list(servers['id'])
        for n, id in enumerate(ids):
            if id.find(serverid) != -1:
                break
            if n >= len(ids)-1:
                return await interaction.response.send_message('No server found!',ephemeral=True)

        try:
            msg = await channel.send(f'# Starfall server\n```roblox://placeId=91355853256093&gameInstanceId={id}```\n-# Sent by {interaction.user.mention}')
        except Exception as e:
            return await interaction.response.send_message(f'ops!\n`{e}`', ephemeral=True)

        await msg.add_reaction('⬆️')
        await msg.add_reaction('⬇️')
        await interaction.response.send_message('Notified!', ephemeral=True)

async def setup(bot:commands.Bot):
    await bot.add_cog(NotifyStarfall(bot))