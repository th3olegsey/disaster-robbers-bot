import discord
from discord.ext import commands
from discord import app_commands

def xp_for_level(level):
    return level * 100 + 1000 if level < 100 else 11000

class XpCalc(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name='calculate',description='Calculates ur XP based on ur level input.')
    @app_commands.describe(level_input='Your level_input',exp_input='Your exp_input',income='How many xp you getting per hour (optional)')
    @app_commands.rename(level_input='level', exp_input='xp')
    async def calculate(self, interaction: discord.Interaction, level_input: str | None, exp_input: int | None, income: int | None):
        if (level_input is None) == (exp_input is None):
            return await interaction.response.send_message('Please enter some data in `level_input` __**or**__ `exp_input`',ephemeral=True)

        if income is None:
            income = 11000

        embed = discord.Embed(title='Calculation results')

        # LEVEL
        if level_input is not None:

            if '-' not in level_input:
                level = int(level_input)
                xp = 0

                while level > 0:
                    xp += xp_for_level(level)
                    level -= 1

                embed.add_field(name='Input values:',value=f'level: `{level_input}`\ngain: `{income}` XP/hr')
                embed.add_field(name='Output values:',value=f'EST: `{xp / income:.2f}` hrs\nXP: `{xp}`')

                return await interaction.response.send_message(embed=embed)

            levels = level_input.split('-')

            if len(levels) != 2:
                return await interaction.response.send_message('Use level range like `50-100`',ephemeral=True)

            start, end = map(int, levels)

            xp_start = sum(xp_for_level(level) for level in range(1, start + 1))
            xp_end = sum(xp_for_level(level) for level in range(1, end + 1))

            xp = xp_end - xp_start

            embed.add_field(name='Input values:',value=f'level: `{level_input}`\ngain: `{income}` XP/hr')
            embed.add_field(name='Output values:',value=f'EST: `{xp / income:.2f}` hrs\nXP: `{xp}`')

            return await interaction.response.send_message(embed=embed)

        # EXP
        if exp_input is not None:
            level = 0
            xp = 0

            while exp_input > xp:
                level += 1
                xp += xp_for_level(level)

            embed.add_field(name='Input values:',value=f'XP: `{exp_input}`')
            embed.add_field(name='Output values:',value=f'level: `{level}`')

            return await interaction.response.send_message(embed=embed)

async def setup(bot:commands.Bot):
    await bot.add_cog(XpCalc(bot))