# BaseCog.py
import logging
from datetime import datetime, timedelta
import discord
from discord.ext import commands
import strings
import random


class BaseCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='hello')
    async def hello(self, ctx):
        logging.info(';hello command received')
        await ctx.send('Hello :)\n' + strings.Images.janet_wave)

    @commands.command(name='clap')
    async def clap(self, ctx):
        logging.info(';clap command received')
        await ctx.send(strings.Images.clap)

    @commands.command(name='stats')
    async def stats(self, ctx: commands.Context):
        logging.info(';stats command received')
        uptime:timedelta = datetime.now() - ctx.bot.init_datetime
        start_time_str = self.bot.init_datetime.strftime("%b %d @ %H:%M %Z")
        uptime_str = f'{uptime.seconds // 3600}h {uptime.seconds // 60}m {uptime.seconds}s'

        await ctx.send(f'```'
                       f'Time Statistics\n'
                       f'Start Time: \t{start_time_str}\n'
                       f'Uptime: \t\t{uptime_str}\n\n'
                       f'Image Statistics\n'
                       f'Reposts:\t\t{self.bot.reposts}\n'
                       f'Embeds: \t\t{self.bot.embeds}\n'
                       f'```')
        pass

    @commands.command(name='give')
    async def give(self, ctx, *args):
        if len(args) < 1:
            await ctx.send('I can\'t give you anything if you don\'t tell me what you want. :)')
            return

        rand = random.randint(0, len(strings.Images.cactus_list) - 1)
        await ctx.send('Here you go. :)\n' + strings.Images.cactus_list[rand])

    @commands.command(name='rule')
    async def rule(self, ctx, *args):
        if not self.check_role(ctx, 'Staff'):
            return

        elif len(args) < 1:
            await ctx.send('Please give a number of the rule you want to view.')

        elif len(args) > 0:
            valid = False
            rule_num = 0
            try:
                rule_num = int(args[0]) - 1
                rules = strings.Files.get_rules()
                valid = rule_num in range(len(rules))
            except ValueError as e:
                await ctx.send('You gave an invalid value for a rule number.')
                logging.error(e)

            if valid:
                rules = strings.Files.get_rules()
                await ctx.send(f'```{rules[rule_num]}```')
            else:
                await ctx.send('That rule number does not exist.')

    @commands.command(name='rules')
    async def rules(self, ctx, *args):
        if not self.check_role(ctx, 'Staff'):
            return
        elif len(args) < 1:
            rules = '```Developer\'s Hub Rules\n\n'
            for rule in strings.Files.get_facts('rules'):
                rules += rule + '\n'
            rules += '```'
            await ctx.send(rules)

    def check_role(self, ctx, role_name):
        guild: discord.Guild = discord.utils.get(self.bot.guilds, name=self.bot.guild_name)
        staff_role = discord.utils.get(guild.roles, name=role_name)
        if staff_role in ctx.author.roles:
            return True
        else:
            return False
