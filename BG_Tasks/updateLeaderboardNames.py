import discord
import aiohttp
import pandas as pd

from discord.ext import tasks,commands
url = 'https://users.roblox.com/v1/users'

class UpdateLeaderboardNames(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
        self.updateLeaderboardNames.start()
    def cog_unload(self):
        self.updateLeaderboardNames.cancel()

    @tasks.loop(minutes=30)
    async def updateLeaderboardNames(self):
        names_csv = pd.read_csv('Data/Guild/Leaderboard/name.csv')
        displays_csv = pd.read_csv('Data/Guild/Leaderboard/display.csv')
        payload = {
            'userIds': names_csv['uid'].to_list()
        }
        async with aiohttp.ClientSession() as s:
            async with s.post(url, json=payload) as r:
                if r.ok:
                    json = await r.json()
                    data = json['data']

                    for i in range(len(names_csv)):
                        ser = names_csv.iloc[i]
                        for k in data:
                            if ser['uid'] == k['id']:
                                ser['value'] = k['name']
                                names_csv.iloc[i] = ser
                    names_csv.to_csv('Data/Guild/Leaderboard/name.csv', index=False, header=True)

                    for i in range(len(displays_csv)):
                        ser = displays_csv.iloc[i]
                        for k in data:
                            if ser['uid'] == k['id']:
                                ser['value'] = k['displayName']
                                displays_csv.iloc[i] = ser
                    displays_csv.to_csv('Data/Guild/Leaderboard/display.csv', index=False, header=True)
                                
async def setup(bot:commands.Bot):
    await bot.add_cog(UpdateLeaderboardNames(bot))