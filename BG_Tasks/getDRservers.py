from discord.ext import commands,tasks
import aiohttp
import pandas as pd
api = 'https://games.roblox.com/v1/games/91355853256093/servers/Public?limit=100'

class GetDRservers(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
        self.getDrServers.start()

    def cog_unload(self):
        self.getDrServers.cancel()

    @tasks.loop(minutes=1)
    async def getDrServers(self):
        async with aiohttp.ClientSession() as s:
            async with s.get(api) as r:
                if r.ok:
                    data = await r.json()
                    servers = data['data']
                    pd.DataFrame(servers).to_csv('data/game/servers.csv', index=False, header=True)

async def setup(bot:commands.Bot):
    await bot.add_cog(GetDRservers(bot))