import discord
from discord import app_commands
from discord.ext import commands
import pandas as pd
from Data.Guild.Users.user import User

class Buttonz(discord.ui.View):
    def __init__(self, id):
        super().__init__(timeout=600)
        self.id = id
        self.upvoted = []
        self.downvoted = []

    async def on_timeout(self):
        for item in self.children:
            item.disabled = True
        await self.msg.edit(view=self)
        score = len(self.upvoted) - len(self.downvoted)
        user = User(self.id)
        rep = user.get_reputation()
        if score > 0:
            user.set_reputation(rep+1)
        else:
            user.set_reputation(rep-1)

    @discord.ui.button(emoji='⬆️', style=discord.ButtonStyle.blurple)
    async def upvote(self, interaction:discord.Interaction, button:discord.Button):
        if (interaction.user.id not in self.upvoted) and (interaction.user.id not in self.downvoted):
            self.upvoted.append(interaction.user.id)
            await interaction.response.send_message('Voted!', ephemeral=True)
        else:
            await interaction.response.send_message('Already voted!', ephemeral=True)
    @discord.ui.button(emoji='⬇️', style=discord.ButtonStyle.blurple)
    async def downvote(self, interaction:discord.Interaction, button:discord.Button):
        if (interaction.user.id not in self.upvoted) and (interaction.user.id not in self.downvoted):
            self.downvoted.append(interaction.user.id)
            await interaction.response.send_message('Voted!', ephemeral=True)
        else:
            await interaction.response.send_message('Already voted!', ephemeral=True)

class NotifyStarfall(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name='notifystarfall', description='Sends notification to the channel')
    async def notify(self, interaction:discord.Interaction, serverid: str):
        user = User(interaction.user.id)
        reputation = user.get_reputation()
        if reputation < -5:
            return await interaction.response.send_message(f'''You are no longer have access to this command.
Reason: Reputation is `{reputation}`
If you wish to appeal uhh just dm me''',ephemeral=True)
        channel = interaction.channel
        servers = pd.read_csv('data/game/servers.csv')
        ids = list(servers['id'])
        for n, id in enumerate(ids):
            if id.find(serverid) != -1:
                break
            if n >= len(ids)-1:
                return await interaction.response.send_message('No server found!',ephemeral=True)
        embed = discord.Embed(title='Starfall server', description=f'```roblox://placeId=91355853256093&gameInstanceId={id}```', color=0xcf0fc0)
        embed.set_author(name=f'Sent by {interaction.user.name}. Reputation: {reputation}')
        view = Buttonz(interaction.user.id)
        try:
            view.msg = await channel.send(embed=embed, view=view)
            await interaction.response.send_message('Notified!', ephemeral=True)
        except Exception as e:
            return await interaction.response.send_message(f'oof\n`{e}`')

async def setup(bot:commands.Bot):
    await bot.add_cog(NotifyStarfall(bot))