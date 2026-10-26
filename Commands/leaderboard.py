import discord
import pandas as pd

from discord import app_commands
from discord.ext import commands
from Data.Guild.Leaderboard.Player import Player
notations = ['', 'k', 'm', 'b']
def formatCash(cash:int) -> str:
    letter = 0
    while(cash > 1000):
        cash /= 1000
        letter += 1
    finalCash = f'{round(cash, 1)}{notations[letter]}'
    return finalCash

def buildLeaderboard(page:int , is_display: bool, sort_by: str):
    the_leaderboard = ''
    name_or_display = 'Name' if not is_display else 'Display'
    main_columns = f' {'№':^3} | {name_or_display:^20} | Lvl | Cash '

    csvNames = pd.read_csv('Data/Guild/Leaderboard/name.csv')
    uids = csvNames['uid'].to_list()
    members = []
    for uid in uids:
        player = Player(uid)
        members.append({
                'name': player.name(),
                'display': player.display(),
                'level': player.level(),
                'cash': player.cash()
            })

    if sort_by == 'level':
        members = sorted(members, key=lambda x: x['level'], reverse=True)
    elif sort_by == 'cash':
        members = sorted(members, key=lambda x: x['cash'], reverse=True)

    players = ''
    for number, member in enumerate(members):
        pos = number + 1
        if pos >= 25 * (page - 1) and pos < 25 * page:
            guy = member['name'] if not is_display else member['display']
            players = f'{players} {(number+1):<3} | {guy:<20} | {member['level']:<3} | {formatCash(member['cash']):<6}\n'

    the_leaderboard = f'{main_columns}\n-----+----------------------+-----+-------\n{players}'
    embed = discord.Embed(title='DR leaderboard', description=f'```\n{the_leaderboard}```')
    embed.set_footer(text=f'Page: {page}')
    return embed

class Buttons(discord.ui.View):
    def __init__(self, page:int, is_display:bool, sort_by:str):
        super().__init__(timeout=300)
        self.sort_by = sort_by
        self.is_display = is_display
        self.page = page

    @discord.ui.button(label='Previous page', emoji='◀️', style=discord.ButtonStyle.success, custom_id='p', disabled=True)
    async def pPage(self, interaction:discord.Interaction, button:discord.Button):
        await interaction.response.defer()
        self.page -= 1
        embed = buildLeaderboard(self.page, self.is_display, self.sort_by)

        pBtn = [x for x in self.children if x.custom_id == 'p'][0]
        pBtn5 = [x for x in self.children if x.custom_id == 'p5'][0]

        pBtn.disabled = True if self.page <= 1 else False 
        pBtn5.disabled = True if self.page <= 5 else False

        await interaction.followup.edit_message(interaction.message.id, embed=embed, view=self)
    @discord.ui.button(label='Next page', emoji='▶️', style=discord.ButtonStyle.success, custom_id='n', disabled=False)
    async def nPage(self, interaction:discord.Interaction, button:discord.Button):
        await interaction.response.defer()
        self.page += 1
        embed = buildLeaderboard(self.page, self.is_display, self.sort_by)

        pBtn = [x for x in self.children if x.custom_id == 'p'][0]
        pBtn5 = [x for x in self.children if x.custom_id == 'p5'][0]

        pBtn.disabled = True if self.page <= 1 else False 
        pBtn5.disabled = True if self.page <= 5 else False

        await interaction.followup.edit_message(interaction.message.id, embed=embed, view=self)
    @discord.ui.button(label='Change name display', emoji='🔁', style=discord.ButtonStyle.blurple, custom_id='change')
    async def changeNameDisplay(self, interaction: discord.Interaction, button:discord.ui.Button):
        await interaction.response.defer()
        self.is_display = not(self.is_display)
        embed = buildLeaderboard(self.page, self.is_display, self.sort_by)
        await interaction.followup.edit_message(interaction.message.id, embed=embed, view=self)
    @discord.ui.button(label='Previous page x5', emoji='◀️', style=discord.ButtonStyle.success, custom_id='p5', disabled=True, row=1)
    async def pPage5(self, interaction: discord.Interaction, button:discord.ui.Button):
        await interaction.response.defer()
        self.page -= 5
        embed = buildLeaderboard(self.page, self.is_display, self.sort_by)

        pBtn = [x for x in self.children if x.custom_id == 'p'][0]
        pBtn5 = [x for x in self.children if x.custom_id == 'p5'][0]

        pBtn.disabled = True if self.page <= 1 else False 
        pBtn5.disabled = True if self.page <= 5 else False

        await interaction.followup.edit_message(interaction.message.id, embed=embed, view=self)
    @discord.ui.button(label='Next page x5', emoji='▶️', style=discord.ButtonStyle.success, custom_id='n5', row=1)
    async def nPage5(self, interaction: discord.Interaction, button:discord.ui.Button):
        await interaction.response.defer()
        self.page += 5
        embed = buildLeaderboard(self.page, self.is_display, self.sort_by)

        pBtn = [x for x in self.children if x.custom_id == 'p'][0]
        pBtn5 = [x for x in self.children if x.custom_id == 'p5'][0]

        pBtn.disabled = True if self.page <= 1 else False 
        pBtn5.disabled = True if self.page <= 5 else False

        await interaction.followup.edit_message(interaction.message.id, embed=embed, view=self)
    @discord.ui.button(label='Sort by $$/Lvl', emoji='🔁', style=discord.ButtonStyle.blurple, custom_id='filter', row=1)
    async def applyFilter(self, interaction: discord.Interaction, button:discord.ui.Button):
        await interaction.response.defer()
        self.sort_by = 'cash' if self.sort_by == 'level' else 'level'
        embed = buildLeaderboard(self.page, self.is_display, self.sort_by)
        await interaction.followup.edit_message(interaction.message.id, embed=embed, view=self)
    

class Leaderboard(commands.Cog):
    def __init__(self,bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name='leaderboard', description='Shows leaderboard')
    @app_commands.choices(sort_by=[app_commands.Choice(name='Level', value='level'),
                                   app_commands.Choice(name='Cash', value='cash')])
    async def leaderboard(self, interaction:discord.Interaction, page: int | None, sort_by: app_commands.Choice[str] | None):
        if page is None:
            page = 1
        if sort_by is None:
            sort_by = app_commands.Choice(name='', value='level')
        embed = buildLeaderboard(page, True, sort_by.value)
        await interaction.response.send_message(embed=embed, view=Buttons(page, True, sort_by.value))
        

async def setup(bot:commands.Bot):
    await bot.add_cog(Leaderboard(bot))


'''
№ | Name | level | cash
--+------+-------+-----
1 | wasd | 99999 | 999b
.......................
25| wasd | 99999 | 999b
'''