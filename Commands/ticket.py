import discord
from discord import app_commands
from discord.ext import commands
import os
#from dotenv import load_dotenv
#load_dotenv()

from Views.Ticket_panel import TicketPanelView

class Ticket(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

        self.bot.add_view(TicketPanelView(bot))

    @app_commands.command(name='ticket_panel', description='Create ticket')
    async def ticket_panel(self, interaction:discord.Interaction):
        if not interaction.user.guild_permissions.administrator:
            return await interaction.response.send_message('nope', ephemeral=True)
        channel = interaction.channel
        embed = discord.Embed(title='Create a ticket',
                              description='Need help? Open a ticket on the appropriate topic.',
                              color=0xFFFFFF)
        embed.set_author(name='The AmmoLoaded Entertainment Team')
        await channel.send(embed=embed, view=TicketPanelView(self.bot))
        await interaction.response.send_message('done', ephemeral=True)

async def setup(bot:commands.Bot):
    await bot.add_cog(Ticket(bot))