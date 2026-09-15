import discord
from discord.ext import commands
from Views.Ticket_Itself import Ticket
import pandas as pd
import os
from dotenv import load_dotenv
load_dotenv()
log_channel_id = int(os.getenv('log_channel_id'))

class AskModal(discord.ui.Modal, title='Question'):
    def __init__(self, bot:commands.Bot):
        super().__init__()
        self.bot = bot
    question = discord.ui.TextInput(label='Question', style=discord.TextStyle.long, placeholder='How to enter raid mode?')
    async def on_submit(self, interaction:discord.Interaction):
        if self.question:
            log_embed = discord.Embed(title='New ticket (Question)',description=f'```{self.question.value}```',color=0x00FF00)
            log_embed.set_author(name=interaction.user.name)
            await interaction.guild.get_channel(log_channel_id).send(embed=log_embed)
            embed = discord.Embed(title='Question',
                                  description=f'```{self.question.value}```',
                                  color=0x00FF00)
            embed.set_author(name=f'From {interaction.user.name}')
            channel = self.bot.get_channel(1523808459680911504)
            await interaction.response.send_message('Thank you for your ticket!', ephemeral=True)
            msg = await channel.send(embed=embed, view=Ticket(self.bot))
            d = [{
                'ticket_id': msg.id,
                'type': 0,
                'id':interaction.user.id,
                'res1': self.question.value,
                'res2': None
            }]
            d = pd.DataFrame(d)
            csv = pd.read_csv('tickets.csv')
            csv = pd.concat([csv,d],ignore_index=True)
            csv.to_csv('tickets.csv', index=False, header=True)

class BugModal(discord.ui.Modal, title='Bug report'):
    def __init__(self, bot:commands.Bot):
        super().__init__()
        self.bot = bot
    bug = discord.ui.TextInput(label='Describe issued bug', style=discord.TextStyle.long, placeholder='This game is laggy. video.mp4')
    async def on_submit(self, interaction:discord.Interaction):
        if self.bug:
            log_embed = discord.Embed(title='New ticket (Bug report)',description=f'```{self.bug.value}```',color=0x00FF00)
            log_embed.set_author(name=interaction.user.name)
            await interaction.guild.get_channel(log_channel_id).send(embed=log_embed)
            embed = discord.Embed(title='Bug report',
                                  description=f'```{self.bug.value}```',
                                  color=0x2596be)
            embed.set_author(name=f'From {interaction.user.name}')
            channel = self.bot.get_channel(1523808459680911504)
            await interaction.response.send_message('Thank you for your ticket!', ephemeral=True)
            msg = await channel.send(embed=embed, view=Ticket(self.bot))
            d = [{
                'ticket_id': msg.id,
                'type': 1,
                'id':interaction.user.id,
                'res1': self.bug.value,
                'res2': None
            }]
            d = pd.DataFrame(d)
            csv = pd.read_csv('tickets.csv')
            csv = pd.concat([csv,d],ignore_index=True)
            csv.to_csv('tickets.csv', index=False, header=True)

class ExploitModal(discord.ui.Modal, title='Exploit report'):
    def __init__(self, bot:commands.Bot):
        super().__init__()
        self.bot = bot
    user = discord.ui.TextInput(label='User', placeholder='hackerman45', min_length=3, max_length=20)
    evidence = discord.ui.TextInput(label='Evidence',placeholder='Youtube or medal link. Keep your evidences unlisted!')
    async def on_submit(self, interaction:discord.Interaction):
        if self.user and self.evidence:
            log_embed = discord.Embed(title='New ticket (Exploit report)',description=f'```{self.user.value}\n{self.evidence.value}```',color=0x00FF00)
            log_embed.set_author(name=interaction.user.name)
            await interaction.guild.get_channel(log_channel_id).send(embed=log_embed)
            embed = discord.Embed(title='Exploit report',
                                  description=f'```{self.user.value}```\n{self.evidence}',
                                  color=0xFF0000)
            embed.set_author(name=f'From {interaction.user.name}')
            channel = self.bot.get_channel(1523808459680911504)
            await interaction.response.send_message('Thank you for your ticket!', ephemeral=True)
            msg = await channel.send(embed=embed, view=Ticket(self.bot))
            d = [{
                'ticket_id': msg.id,
                'type': 2,
                'id':interaction.user.id,
                'res1': self.user.value,
                'res2': self.evidence.value
            }]
            d = pd.DataFrame(d)
            csv = pd.read_csv('tickets.csv')
            csv = pd.concat([csv,d],ignore_index=True)
            csv.to_csv('tickets.csv', index=False, header=True)

class TicketPanelView(discord.ui.View):
    def __init__(self, bot:commands.Bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(label='Ask question', style=discord.ButtonStyle.green, custom_id='ask_button')
    async def ask(self, interaction:discord.Interaction, button:discord.Button):
        await interaction.response.send_modal(AskModal(self.bot)) #type 0

    @discord.ui.button(label='Bug report', style=discord.ButtonStyle.blurple, custom_id='bug_button')
    async def bugreport(self, interaction:discord.Interaction, button:discord.Button):
        await interaction.response.send_modal(BugModal(self.bot)) #type 1

    @discord.ui.button(label='Exploit report', style=discord.ButtonStyle.red, custom_id='hack_button')
    async def hackreport(self, interaction:discord.Interaction, button:discord.Button):
        await interaction.response.send_modal(ExploitModal(self.bot)) #type 2