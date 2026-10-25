import discord

from discord.ext import commands

class LogEveryCommand (commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_interaction(self ,interaction: discord.Interaction):
        log_channel = await self.bot.fetch_channel(1495456107081105470)
        if interaction.command != None and interaction.type == discord.InteractionType.application_command:
            esc = chr(27)
            if interaction.data.__contains__('options'):
                params = ''
                for i in interaction.data['options']:
                    params = f'{params}{i['value']} '
                await log_channel.send(f'```ansi\n{esc}[1;34m{interaction.user}{esc}[0m: {esc}[1;31m{interaction.data["name"]}{esc}[0m {esc}[1;33m{params}{esc}[0m```')
            else:
                await log_channel.send(f'```ansi\n{esc}[1;34m{interaction.user}{esc}[0m: {esc}[1;31m{interaction.data["name"]}{esc}[0m```')

async def setup(bot:commands.Bot):
    await bot.add_cog(LogEveryCommand(bot))