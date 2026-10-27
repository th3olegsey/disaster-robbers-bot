import discord
import pandas as pd

from PIL import Image, ImageDraw, ImageFont
from discord import app_commands
from discord.ext import commands
from io import BytesIO
from Data.Guild.Leaderboard.Player import Player
linethickness = 3
font = ImageFont.truetype("consola.ttf", size=15)
notations = ['', 'k', 'm', 'b']
def formatCash(cash:int) -> str:
    letter = 0
    while(cash > 1000):
        cash /= 1000
        letter += 1
    finalCash = f'{round(cash, 1)}{notations[letter]}'
    return finalCash

def buildLeaderboard(page:int , is_display: bool, sort_by: str) -> str:
    the_leaderboard = ''
    the_places = ''
    the_guys = ''
    the_levels = ''
    the_cash = ''

    name_or_display = 'Display' if is_display else 'Name'
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

    members = sorted(members, key=lambda x: x['level'] if sort_by == 'level' else x['cash'], reverse=True)

    players = ''
    for number, member in enumerate(members):
        pos = number + 1
        if pos >= 25 * (page - 1) and pos < 25 * page:
            guy = member['display'] if is_display else member['name']
            players = f'{players} {(pos):<3} | {guy:<20} | {member['level']:<3} | {formatCash(member['cash']):<6}\n'

            the_places = f'{the_places}{pos}\n'
            the_guys = f'{the_guys}{guy}\n'
            the_levels = f'{the_levels}{member['level']}\n'
            the_cash = f'{the_cash}{formatCash(member['cash'])}\n'


    the_leaderboard = f'{main_columns}\n-----+----------------------+-----+-------\n{players}'
    return the_leaderboard, the_places, the_guys, the_levels, the_cash

def lbToEmbed(the_leaderboard, page) -> discord.Embed:
    embed = discord.Embed(title='DR leaderboard', description=f'```\n{the_leaderboard}```')
    embed.set_footer(text=f'Page: {page}')
    return embed

def lbToImage(the_places:str, is_display:bool, the_guys:str, the_levels:str, the_cash:str) -> discord.File:
    name_or_display = 'Display' if is_display else 'Name'
    img = Image.new('RGB', (370,440), 0xFFFFFF)

    idraw = ImageDraw.Draw(img)
    idraw.text((35,20), '№', font=font, fill=0x000000, align='m')
    idraw.text((125,20), name_or_display, font=font, fill=0x000000, align='m')
    idraw.text((242,20), 'Level', font=font, fill=0x000000, align='m')
    idraw.text((305,20), 'Cash', font=font, fill=0x000000, align='m')

    idraw.rectangle((15, 40, 355, 40+linethickness), fill=0x000000)
    idraw.rectangle((60, 20, 60+linethickness, 430), fill=0x000000)
    idraw.rectangle((235, 20, 235+linethickness, 430), fill=0x000000)
    idraw.rectangle((285, 20, 285+linethickness, 430), fill=0x000000)

    idraw.text((25,50), the_places, font=font, fill=0x000000)
    idraw.text((70,50), the_guys, font=font, fill=0x000000)
    idraw.text((245,50), the_levels, font=font, fill=0x000000)
    idraw.text((295,50), the_cash, font=font, fill=0x000000)

    img_bin = BytesIO()
    img.save(img_bin, 'png')
    img_bin.seek(0)
    file = discord.File(img_bin,'leaderboard.png')
    return file

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

        the_leaderboard, the_places, the_guys, the_levels, the_cash = buildLeaderboard(self.page, self.is_display, self.sort_by)
        file = lbToImage(the_places, self.is_display, the_guys, the_levels, the_cash)
        embed = discord.Embed(title='DR leaderboard')
        embed.set_image(url='attachment://leaderboard.png')
        embed.set_footer(text=f'Page: {self.page}')

        pBtn = [x for x in self.children if x.custom_id == 'p'][0]
        pBtn5 = [x for x in self.children if x.custom_id == 'p5'][0]

        pBtn.disabled = True if self.page <= 1 else False 
        pBtn5.disabled = True if self.page <= 5 else False

        await interaction.followup.edit_message(interaction.message.id, attachments=[file], embed=embed, view=self)
    @discord.ui.button(label='Next page', emoji='▶️', style=discord.ButtonStyle.success, custom_id='n', disabled=False)
    async def nPage(self, interaction:discord.Interaction, button:discord.Button):
        await interaction.response.defer()
        self.page += 1
        the_leaderboard, the_places, the_guys, the_levels, the_cash = buildLeaderboard(self.page, self.is_display, self.sort_by)
        file = lbToImage(the_places, self.is_display, the_guys, the_levels, the_cash)
        embed = discord.Embed(title='DR leaderboard')
        embed.set_image(url='attachment://leaderboard.png')
        embed.set_footer(text=f'Page: {self.page}')

        pBtn = [x for x in self.children if x.custom_id == 'p'][0]
        pBtn5 = [x for x in self.children if x.custom_id == 'p5'][0]

        pBtn.disabled = True if self.page <= 1 else False 
        pBtn5.disabled = True if self.page <= 5 else False

        await interaction.followup.edit_message(interaction.message.id, attachments=[file], embed=embed, view=self)
    @discord.ui.button(label='Change name display', emoji='🔁', style=discord.ButtonStyle.blurple, custom_id='change')
    async def changeNameDisplay(self, interaction: discord.Interaction, button:discord.ui.Button):
        await interaction.response.defer()
        self.is_display = not(self.is_display)
        the_leaderboard, the_places, the_guys, the_levels, the_cash = buildLeaderboard(self.page, self.is_display, self.sort_by)
        file = lbToImage(the_places, self.is_display, the_guys, the_levels, the_cash)
        embed = discord.Embed(title='DR leaderboard')
        embed.set_image(url='attachment://leaderboard.png')
        embed.set_footer(text=f'Page: {self.page}')

        await interaction.followup.edit_message(interaction.message.id, attachments=[file], embed=embed, view=self)
    @discord.ui.button(label='Previous page x5', emoji='◀️', style=discord.ButtonStyle.success, custom_id='p5', disabled=True, row=1)
    async def pPage5(self, interaction: discord.Interaction, button:discord.ui.Button):
        await interaction.response.defer()
        self.page -= 5
        the_leaderboard, the_places, the_guys, the_levels, the_cash = buildLeaderboard(self.page, self.is_display, self.sort_by)
        file = lbToImage(the_places, self.is_display, the_guys, the_levels, the_cash)
        embed = discord.Embed(title='DR leaderboard')
        embed.set_image(url='attachment://leaderboard.png')
        embed.set_footer(text=f'Page: {self.page}')

        pBtn = [x for x in self.children if x.custom_id == 'p'][0]
        pBtn5 = [x for x in self.children if x.custom_id == 'p5'][0]

        pBtn.disabled = True if self.page <= 1 else False 
        pBtn5.disabled = True if self.page <= 5 else False

        await interaction.followup.edit_message(interaction.message.id, attachments=[file], embed=embed, view=self)
    @discord.ui.button(label='Next page x5', emoji='▶️', style=discord.ButtonStyle.success, custom_id='n5', row=1)
    async def nPage5(self, interaction: discord.Interaction, button:discord.ui.Button):
        await interaction.response.defer()
        self.page += 5
        the_leaderboard, the_places, the_guys, the_levels, the_cash = buildLeaderboard(self.page, self.is_display, self.sort_by)
        file = lbToImage(the_places, self.is_display, the_guys, the_levels, the_cash)
        embed = discord.Embed(title='DR leaderboard')
        embed.set_image(url='attachment://leaderboard.png')
        embed.set_footer(text=f'Page: {self.page}')

        pBtn = [x for x in self.children if x.custom_id == 'p'][0]
        pBtn5 = [x for x in self.children if x.custom_id == 'p5'][0]

        pBtn.disabled = True if self.page <= 1 else False 
        pBtn5.disabled = True if self.page <= 5 else False

        await interaction.followup.edit_message(interaction.message.id, attachments=[file], embed=embed, view=self)
    @discord.ui.button(label='Sort by $$/Lvl', emoji='🔁', style=discord.ButtonStyle.blurple, custom_id='sort', row=1)
    async def sortLB(self, interaction: discord.Interaction, button:discord.ui.Button):
        await interaction.response.defer()
        self.sort_by = 'cash' if self.sort_by == 'level' else 'level'
        the_leaderboard, the_places, the_guys, the_levels, the_cash = buildLeaderboard(self.page, self.is_display, self.sort_by)
        file = lbToImage(the_places, self.is_display, the_guys, the_levels, the_cash)
        embed = discord.Embed(title='DR leaderboard')
        embed.set_image(url='attachment://leaderboard.png')
        embed.set_footer(text=f'Page: {self.page}')
        await interaction.followup.edit_message(interaction.message.id, attachments=[file], embed=embed, view=self)
    @discord.ui.button(label='Show as text', emoji='🔤', style=discord.ButtonStyle.gray, custom_id='text', row=2)
    async def lbAsText(self, intecation:discord.Interaction, button:discord.Button):
        the_leaderboard, the_places, the_guys, the_levels, the_cash = buildLeaderboard(self.page, self.is_display, self.sort_by)
        await intecation.response.send_message(f'```\n{the_leaderboard}```', ephemeral=True)

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

        the_leaderboard, the_places, the_guys, the_levels, the_cash = buildLeaderboard(page, True, sort_by.value)
        file = lbToImage(the_places,True,the_guys,the_levels,the_cash)
        embed = discord.Embed(title='DR leaderboard')
        embed.set_image(url='attachment://leaderboard.png')
        embed.set_footer(text=f'Page: {page}')
        await interaction.response.send_message(file=file, embed=embed, view=Buttons(page, True, sort_by.value))

async def setup(bot:commands.Bot):
    await bot.add_cog(Leaderboard(bot))