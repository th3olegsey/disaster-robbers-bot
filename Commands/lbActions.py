import discord
from roblox import Client
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

class LbActionModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title='Submit a leaderboard request...')
    actionType = discord.ui.Label(text='Action', component=LbActionsDropdown())
    name = discord.ui.TextInput(label='User', placeholder='Toiebe')
    rank = discord.ui.TextInput(label='Rank', placeholder='100', required=False)
    cash = discord.ui.TextInput(label='Cash', placeholder='402350', required=False)
    async def on_submit(self, interaction:discord.Interaction):
        if self.rank.value:
            if not self.rank.value.isdecimal():
                return await interaction.response.send_message('Rank should be an interger!', ephemeral=True)
        if self.cash.value:
            if not self.cash.value.isdecimal():
                return await interaction.response.send_message('Cash should be an interger!', ephemeral=True)
            
        uid = 0
        client = Client()
        async for user in client.user_search(self.name.value,max_items=1):
            uid = user.id
        if uid:
            player = Player(int(uid))
            if self.actionType.component.values[0] == 'a':
                player.add(int(self.rank.value), int(self.cash.value))
                await interaction.response.send_message('Added!', ephemeral=True)
            elif self.actionType.component.values[0] == 'e':
                player.edit(int(self.rank.value), int(self.cash.value))
                await interaction.response.send_message('Edited!', ephemeral=True)
            elif self.actionType.component.values[0] == 'd':
                player.delete()
                await interaction.response.send_message('Deleted!', ephemeral=True)
        else:
            return await interaction.response.send_message('User not found')

class LbActions(commands.Cog):
    def __init__(self, bot:commands.bot):
        self.bot = bot

    @app_commands.command(name='lbactions')
    async def lbActions(self, interaction:discord.Interaction):
        if interaction.user.id != 884134020693229639:
            return await interaction.response.send_message('You are not th3_olegsey', ephemeral=True)
        await interaction.response.send_modal(LbActionModal())

async def setup(bot:commands.Bot):
    await bot.add_cog(LbActions(bot))