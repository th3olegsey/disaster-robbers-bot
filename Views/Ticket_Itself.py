import discord
from discord.ext import commands
import pandas as pd
import os
from dotenv import load_dotenv
load_dotenv()
log_channel_id = int(os.getenv('log_channel_id'))
ticket_types={
    0: "Question",
    1: "Bug report",
    2: "Exploit report"
}
class CommentModal(discord.ui.Modal, title='Add comment'):
    def __init__(self, bot:commands.Bot, accepted:bool):
        super().__init__()
        self.bot = bot
        self.accepted = accepted
        self.comment = discord.ui.TextInput(label='Enter a comment',
                                            style=discord.TextStyle.long,
                                            placeholder='Thx for your ticket!',
                                            required=False if accepted else True)
        self.add_item(self.comment)
    async def on_submit(self, interaction:discord.Interaction):
        id = interaction.message.id
        csv = pd.read_csv('tickets.csv')
        k = 0
        while(k <= len(csv)):
            if csv.iloc[k]['ticket_id'] == id:
                ticket = csv.iloc[k]
                csv = csv.loc[csv['ticket_id'] != id]
                csv.to_csv('tickets.csv', index=False, header=True)
                break
            k += 1

        if self.accepted:
            msg = 'Your ticket has been accepted'
            if self.comment.value:
                msg = f'{msg}\nAdditional info from staff: {self.comment.value}'
            user = self.bot.get_user(ticket['id'])
            log_embed = discord.Embed(title=f'Accepted ticket ({ticket_types[ticket['type']]})')
        elif not self.accepted:
            msg = 'Your ticket has been declined'
            if self.comment.value:
                msg = f'{msg}\nAdditional info from staff: {self.comment.value}'
            user = self.bot.get_user(ticket['id'])
            log_embed = discord.Embed(title=f'Declined ticket ({ticket_types[ticket['type']]})')

        if not self.comment.value:
            self.comment.value = '[ None ]'

        log_embed.description = f'```{ticket['res1']}```\n```{ticket['res2']}```\ncomment:\n```{self.comment.value}```'
        log_embed.color = 0x0000FF
        log_embed.set_author(name=interaction.user.name)

        await interaction.guild.get_channel(log_channel_id).send(embed=log_embed)
        await user.send(msg)
        await interaction.response.send_message('The answer was given', ephemeral=True)
        await interaction.message.delete()


class Ticket(discord.ui.View):
    def __init__(self,bot:commands.Bot):
        super().__init__(timeout=None)
        self.bot = bot
    @discord.ui.button(label='Accept', style=discord.ButtonStyle.green, custom_id='accept')
    async def accept(self, interaction:discord.Interaction, button:discord.Button):
        await interaction.response.send_modal(CommentModal(self.bot, True))
    @discord.ui.button(label='Decline', style=discord.ButtonStyle.gray, custom_id='decline')
    async def decline(self, interaction:discord.Interaction, button:discord.Button):
        await interaction.response.send_modal(CommentModal(self.bot, False))