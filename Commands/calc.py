import discord
from discord.ext import commands
from discord import app_commands

def xp_for_level_s1(level):
    return level * 100 + 1000 if level < 100 else 11000

def xp_for_level_s1u(level):
    return level * 100 + 1000

class Calc(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name='calculate',description='Calculates something based on user\'s input.')
    @app_commands.choices(what_to_calculate=[app_commands.Choice(name='EXP (enter your level)', value='exp'),
                                             app_commands.Choice(name='Level (enter yout EXP)', value='level')])
    @app_commands.choices(formula=[app_commands.Choice(name='Season 1 capped (11k)', value='s1'),
                                   app_commands.Choice(name='Season 1 uncapped', value='s1u')])
    @app_commands.describe(exp_gain='Used for EXP calculation (optional)')
    async def calculate(self, interaction: discord.Interaction, what_to_calculate: app_commands.Choice[str], input: str, formula: app_commands.Choice[str] | None, exp_gain: int | None):

        if exp_gain is None:
            exp_gain = 13000
        if formula is None:
            formula = app_commands.Choice(name='', value='s1')

        embed = discord.Embed(title='Calculation results')

        # LEVEL
        if what_to_calculate.value == 'exp':

            if '-' not in input:
                level = int(input)
                xp = 0

                while level > 0:
                    if formula.value == 's1':
                        xp += xp_for_level_s1(level)
                    elif formula.value == 's1u':
                        xp += xp_for_level_s1u(level)
                    level -= 1

                embed.add_field(name='Input values:',value=f'level: `{input}`\nformula: `{formula.value}`\ngain: `{exp_gain}` XP/hr')
                embed.add_field(name='Output values:',value=f'XP: `{xp}`\nEST: `{xp / exp_gain:.2f}` hrs')

                return await interaction.response.send_message(embed=embed)

            levels = input.split('-')

            if len(levels) != 2:
                return await interaction.response.send_message('Use level range like `50-100`',ephemeral=True)

            start, end = map(int, levels)
            if formula.value == 's1':
                xp_start = sum(xp_for_level_s1(level) for level in range(1, start + 1))
                xp_end = sum(xp_for_level_s1(level) for level in range(1, end + 1))
            elif formula.value == 's1u':
                xp_start = sum(xp_for_level_s1u(level) for level in range(1, start + 1))
                xp_end = sum(xp_for_level_s1u(level) for level in range(1, end + 1))

            xp = xp_end - xp_start

            embed.add_field(name='Input values:',value=f'level: `{input}`\ngain: `{exp_gain}` XP/hr')
            embed.add_field(name='Output values:',value=f'EST: `{xp / exp_gain:.2f}` hrs\nXP: `{xp}`')

            return await interaction.response.send_message(embed=embed)

        # EXP
        if what_to_calculate.value == 'level':
            try:
                input = int(input)
            except:
                return await interaction.response.send_message('Enter an interger!')
            level = 0
            xp = 0

            while input > xp:
                level += 1
                if formula.value == 's1':
                    xp += xp_for_level_s1(level)
                elif formula.value == 's1u':
                    xp += xp_for_level_s1u(level)

            embed.add_field(name='Input values:',value=f'XP: `{input}`')
            embed.add_field(name='Output values:',value=f'level: `{level}`')

            return await interaction.response.send_message(embed=embed)
        # MONEY
        if what_to_calculate.value == 'money':
            return await interaction.response.send_message('work in progress', ephemeral=True)
            all_weapons = 0

            all_vehicles = 2990000 # 2.99m

            all_skins = 468000
            all_colors = 30000
            all_rims = 270050 # why
            all_tires = 30000
            underglow = 100000
            all_boosts = 180000
            all_plates = 25000
            all_spoilers = 90000
            all_hats = 117000
            all_engines = 170000
            all_suspensions = 15000

            all_decorations = all_skins+all_colors+all_rims+all_tires+underglow+all_boosts+all_plates+all_spoilers+all_hats+all_engines+all_suspensions #1495050 or 1.4m

async def setup(bot:commands.Bot):
    await bot.add_cog(Calc(bot))