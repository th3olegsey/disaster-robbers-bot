import discord
from discord.utils import MISSING
import pandas as pd

from PIL import Image, ImageDraw, ImageFont
from discord import app_commands
from discord.ext import commands
from io import BytesIO
from Data.Guild.Leaderboard.Player import Player

linethickness = 3
font = ImageFont.truetype("consola.ttf", size=15)
img_size = {'x':370 ,'y':460}
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
    img = Image.new('RGB', (img_size['x'],img_size['y']), (62, 63, 80))

    idraw = ImageDraw.Draw(img)

    first_line = {'x':15, 'y':30}
    second_line = {'x':60, 'y':10}
    third_line = {'x':235, 'y':10}
    fourth_line = {'x':285, 'y':10}

    idraw.rectangle((first_line['x'], first_line['y'],  img_size['x']-10,              30+linethickness),fill=0xFFFFFF) # ---
    idraw.rectangle((second_line['x'],second_line['y'], second_line['x']+linethickness,img_size['y']-10),fill=0xFFFFFF) # | 1
    idraw.rectangle((third_line['x'], third_line['y'],  third_line['x']+linethickness, img_size['y']-10),fill=0xFFFFFF) # | 2
    idraw.rectangle((fourth_line['x'],fourth_line['y'], fourth_line['x']+linethickness,img_size['y']-10),fill=0xFFFFFF) # | 3

    placeTextPos = (first_line['x'] + second_line['x'])//2
    nodTextPos =   (second_line['x'] + third_line['x'] + linethickness*2)//2
    levelTextPos = (third_line['x'] + fourth_line['x'] + linethickness*2)//2
    cashTextPos =  (fourth_line['x'] + img_size['x']-10 + linethickness*2)//2

    idraw.text((placeTextPos,10),'№',            font=font, anchor='mt')
    idraw.text((nodTextPos,10),  name_or_display,font=font, anchor='mt')
    idraw.text((levelTextPos,10),'Lvl',          font=font, anchor='mt')
    idraw.text((cashTextPos,10), 'Cash',         font=font, anchor='mt')

    idraw.text((25,40), the_places,font=font, fill=(201, 92, 94), stroke_width=.5)
    idraw.text((70,40), the_guys,  font=font, fill=(68, 125, 198),stroke_width=.5)
    idraw.text((245,40),the_levels,font=font, fill=(172, 113, 23),stroke_width=.5)
    idraw.text((295,40),the_cash,  font=font, fill=(72, 146, 101),stroke_width=.5)

    img_bin = BytesIO()
    img.save(img_bin, 'png')
    img_bin.seek(0)
    file = discord.File(img_bin,'leaderboard.png')
    return file

class NameFilterSelect(discord.ui.Select):
    def __init__(self):
        super().__init__(options=[
            discord.SelectOption(label='Display names', value=True),
            discord.SelectOption(label='Names', value=False)],
            required=False,

        )

class SortBySelect(discord.ui.Select):
    def __init__(self):
        super().__init__(options=[
            discord.SelectOption(label='Level', emoji='⭐', value='level',),
            discord.SelectOption(label='Cash', emoji='💲', value='cash')],
            required=False
        )

class SelectPageModal(discord.ui.Modal):
    def __init__(self, is_display:bool, sort_by:str):
        super().__init__(title='Select page')
        self.is_display = is_display
        self.sort_by = sort_by
    page = discord.ui.TextInput(label='Enter page', placeholder='2', required=False)
    async def on_submit(self, interaction:discord.Interaction):
        await interaction.response.defer()
        if not self.page.value.isdigit():
            return await interaction.followup.send('Page value must be an integer!', ephemeral=True)
        page = int(self.page.value) if self.page.value else 1
        _, the_places, the_guys, the_levels, the_cash = buildLeaderboard(page, self.is_display, self.sort_by)
        file = lbToImage(the_places, self.is_display, the_guys, the_levels, the_cash)
        embed = discord.Embed(title='DR leaderboard')
        embed.set_image(url='attachment://leaderboard.png')
        embed.set_footer(text=f'Page: {page}')

        #pBtn = [x for x in self.children if x.custom_id == 'p'][0]
        #pBtn.disabled = True if self.page <= 1 else False 

        await interaction.followup.edit_message(interaction.message.id, attachments=[file], embed=embed, view=Buttons(page, self.is_display, self.sort_by))

class ApplyFilterModal(discord.ui.Modal):
    def __init__(self, page:int):
        super().__init__(title='Apply filter')
        self.page = page
    sort_by = discord.ui.Label(text='Sort by ...', component=SortBySelect())
    is_display = discord.ui.Label(text='Show ...', component=NameFilterSelect())
    async def on_submit(self, interaction:discord.Interaction):
        await interaction.response.defer()

        sort_by_selected = self.sort_by.component.values[0] if len(self.sort_by.component.values) else 'level'
        is_display_selected = self.is_display.component.values[0] == 'True' if len(self.is_display.component.values) else True

        _, the_places, the_guys, the_levels, the_cash = buildLeaderboard(self.page, is_display_selected, sort_by_selected)
        file = lbToImage(the_places, is_display_selected, the_guys, the_levels, the_cash)
        embed = discord.Embed(title='DR leaderboard')
        embed.set_image(url='attachment://leaderboard.png')
        embed.set_footer(text=f'Page: {self.page}')
        await interaction.followup.edit_message(interaction.message.id, attachments=[file], embed=embed, view=Buttons(self.page, is_display_selected, sort_by_selected))

class Buttons(discord.ui.View):
    def __init__(self, page:int, is_display:bool, sort_by:str):
        super().__init__(timeout=300)
        self.sort_by = sort_by
        self.is_display = is_display
        self.page = page

        self.pPage.disabled = self.page <= 1

    @discord.ui.button(emoji='◀️', style=discord.ButtonStyle.success, custom_id='p')
    async def pPage(self, interaction:discord.Interaction, button:discord.Button):
        await interaction.response.defer()
        self.page -= 1

        _, the_places, the_guys, the_levels, the_cash = buildLeaderboard(self.page, self.is_display, self.sort_by)
        file = lbToImage(the_places, self.is_display, the_guys, the_levels, the_cash)
        embed = discord.Embed(title='DR leaderboard')
        embed.set_image(url='attachment://leaderboard.png')
        embed.set_footer(text=f'Page: {self.page}')

        pBtn = [x for x in self.children if x.custom_id == 'p'][0]
        pBtn.disabled = True if self.page <= 1 else False 

        await interaction.followup.edit_message(interaction.message.id, attachments=[file], embed=embed, view=self)
    @discord.ui.button(label='Select page', style=discord.ButtonStyle.success, custom_id='sp')
    async def selectPage(self, interaction:discord.Interaction, button:discord.Button):
        await interaction.response.send_modal(SelectPageModal(self.is_display, self.sort_by))

    @discord.ui.button(emoji='▶️', style=discord.ButtonStyle.success, custom_id='n', disabled=False)
    async def nPage(self, interaction:discord.Interaction, button:discord.Button):
        await interaction.response.defer()
        self.page += 1
        _, the_places, the_guys, the_levels, the_cash = buildLeaderboard(self.page, self.is_display, self.sort_by)
        file = lbToImage(the_places, self.is_display, the_guys, the_levels, the_cash)
        embed = discord.Embed(title='DR leaderboard')
        embed.set_image(url='attachment://leaderboard.png')
        embed.set_footer(text=f'Page: {self.page}')

        pBtn = [x for x in self.children if x.custom_id == 'p'][0]
        pBtn.disabled = True if self.page <= 1 else False 

        await interaction.followup.edit_message(interaction.message.id, attachments=[file], embed=embed, view=self)
    @discord.ui.button(label='Apply filter', emoji='<:filter:1566054560806477825>', style=discord.ButtonStyle.blurple, custom_id='filter', row=2)
    async def applyFilter(self, interaction:discord.Interaction, button:discord.Button):
        await interaction.response.send_modal(ApplyFilterModal(self.page))

    @discord.ui.button(label='Show as text', emoji='🔤', style=discord.ButtonStyle.gray, custom_id='text', row=2)
    async def lbAsText(self, intecation:discord.Interaction, button:discord.Button):
        the_leaderboard, _, _, _, _ = buildLeaderboard(self.page, self.is_display, self.sort_by)
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

        _, the_places, the_guys, the_levels, the_cash = buildLeaderboard(page, True, sort_by.value)
        file = lbToImage(the_places,True,the_guys,the_levels,the_cash)
        embed = discord.Embed(title='DR leaderboard')
        embed.set_image(url='attachment://leaderboard.png')
        embed.set_footer(text=f'Page: {page}')
        await interaction.response.send_message(file=file, embed=embed, view=Buttons(page, True, sort_by.value))

async def setup(bot:commands.Bot):
    await bot.add_cog(Leaderboard(bot))