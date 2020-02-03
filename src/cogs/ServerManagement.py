import logging
import discord
from discord.ext import commands

import verifiers


class ServerManagement(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='delete')
    async def delete(self, ctx, *args):
        def check_author(m): return m.author == ctx.author

        if ctx.guild is not None:
            if not self.check_role(ctx, 'Staff') and ctx.guild.name == 'Developers Hub':
                await ctx.send('Only staff can use delete.')
                return
            elif not self.check_role(ctx, 'me') and ctx.guild.name == 'Indys Corner':
                await ctx.send('Only Indy can use delete here.')
                return

        elif not len(args) > 0:
            await ctx.send('Please give an amount of messages to delete.')
            return

        elif not verifiers.integer(args[0]):
            await ctx.send('Please give a valid integer.')
            return

        delete_amount = int(args[0])
        delete_messages = []
        async for message in ctx.channel.history(limit=delete_amount):
            delete_messages.append(message)

        for message in delete_messages:
            logging.info(message.content)

        await ctx.send(f'Are you sure you want to delete {delete_amount} messages? (`y/n`)')
        message = await self.bot.wait_for('message', check=check_author)
        words = message.content.split()

        if words[0] == 'y':
            async for message in ctx.channel.history(limit=2):
                delete_messages.append(message)

            await ctx.channel.delete_messages(delete_messages)

    def check_role(self, ctx, role_name):
        guild: discord.Guild = discord.utils.get(self.bot.guilds, name=self.bot.guild_name)
        staff_role = discord.utils.get(guild.roles, name=role_name)

        if staff_role in ctx.author.roles:
            return True
        else:
            return False