import discord
import roblox
from discord import app_commands
from discord.ext import commands
from Data.Guild.Leaderboard.Player import Player

class LbActionsDropdown(discord.ui.Select):
    def __init__(self):
        super().__init__(
            options=[
                discord.SelectOption(label='Add', value='a', description='Adds player to the leaderboard', emoji='➕'),
                discord.SelectOption(label='Edit', value='e', description='Edits players on the leaderboard', emoji='🔨'),
                discord.SelectOption(label='Delete', value='d', description='Removes player on the leaderboard', emoji='❌')
            ]
        )

class Lb_request_modal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title='Submit a leaderboard request...')
    actionType = discord.ui.Label(text='Action', component=LbActionsDropdown())
    name = discord.ui.TextInput(label='User', placeholder='Toiebe')
    rank = discord.ui.TextInput(label='Rank', placeholder='100', required=False)
    cash = discord.ui.TextInput(label='Cash', placeholder='402350', required=False)
    #proof = ...
    async def on_submit(self, interaction:discord.Interaction):
        player = Player(self.name.value)
        if self.actionType.component.values[0] == 'a':
            player.add(self.rank, self.cash)
            await interaction.response.send_message('added', ephemeral=True)
        elif self.actionType.component.values[0] == 'e':
            player.edit(self.rank, self.cash)
            await interaction.response.send_message('edited', ephemeral=True)
        elif self.actionType.component.values[0] == 'd':
            player.delete()
            await interaction.response.send_message('deleted', ephemeral=True)

class LbActions(commands.Cog):
    def __init__(self, bot:commands.bot):
        self.bot = bot

    @app_commands.command(name='lbactions')
    async def lbActions(self, interaction:discord.Interaction):
        await interaction.response.send_modal(Lb_request_modal())

async def setup(bot:commands.Bot):
    await bot.add_cog(LbActions(bot))