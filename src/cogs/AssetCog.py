from discord.ext import commands


class AssetCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='asset')
    async def asset(self, ctx, *args):
        pass
