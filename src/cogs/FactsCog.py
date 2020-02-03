import logging
from datetime import datetime, timedelta
import discord
from discord.ext import commands
import strings
from strings import staff_ids
import random
from pathlib import Path


import verifiers


class FactsCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='fact')
    async def fact_command(self, ctx, *args):
        place = 'on ' + ctx.guild.name if ctx.guild is not None else 'in a private message'
        logging.info(f';fact command received from {ctx.author.display_name} {place}')

        if not len(args) > 0:
            await ctx.send('Please provide a valid fact type.')
            return

        filename = args[0].lower()
        texts_path = Path.cwd() / Path('facts')
        file_path = texts_path / Path(filename + '.txt')

        if ctx.author.id in staff_ids.keys():
            if ctx.author.id == staff_ids[filename]:
                await ctx.send('That\'s you silly. ;)')
                return

        if len(args) > 1:
            if args[1] == 'add':
                await self.add(ctx, args[0], args)
                return
            elif args[1] == 'remove':
                await self.remove(ctx, args[0], args)
                return
            elif args[1] == 'list':
                await self.list(ctx, args[0])
                return
            elif args[1] == 'edit':
                await self.edit(ctx, args[0], args)
                return
            elif args[0] == 'create':
                await self.create(ctx, args[1])
                return

        if file_path not in [x for x in texts_path.iterdir()] and args[0] != 'create':
            await ctx.send('Please provide a valid fact type.')
            return

        if ctx.guild is not None and filename in staff_ids.keys():
            if not self.check_role(ctx, 'Staff') and ctx.guild.name == 'Developers Hub':
                await ctx.send('You cannot use this command.')
                return

        if ctx.guild is not None and len(args) > 1:
            if not self.check_role(ctx, 'Staff') and ctx.guild.name == 'Developers Hub':
                return

        await self.get_fact(ctx, filename, 0, *args)

    @staticmethod
    async def add(ctx, filename, words):
        words = words[2:]
        fact = ''
        for word in words:
            fact += word + ' '

        strings.Files.add_fact(filename.lower(), fact)
        await ctx.send(f'Added to facts:```{fact}```')

    @staticmethod
    async def remove(ctx, filename, words):
        facts, facts_str = strings.Files.get_facts(filename.lower())

        if verifiers.integer(words[2], len(facts)):
            choice = int(words[2])
        else:
            await ctx.send('Provide a valid option to remove.')
            return

        removed_fact = facts[choice]
        del facts[choice]

        strings.Files.write_facts(filename.lower(), facts)

        await ctx.send(f'Removed fact:```{removed_fact}```')

    async def edit(self, ctx, filename, words):
        facts, facts_str = strings.Files.get_facts(filename.lower())

        if verifiers.integer(words[2], len(facts)):
            choice = int(words[2])
        else:
            await ctx.send('Provide a valid option to remove.')
            return

        words = words[3:]
        new_fact = ''
        for word in words:
            new_fact += word + ' '
        new_fact += '\n'

        facts[choice] = new_fact
        strings.Files.write_facts(filename.lower(), facts)
        await ctx.send(f'Edited {filename.capitalize()} fact #{choice} to:```{new_fact}```')

    @staticmethod
    async def list(ctx, filename):
        facts, facts_str = strings.Files.get_facts(filename.lower())
        await ctx.send(facts_str)

    async def create(self, ctx, filename: str):
        def check_author(m): return m.author == ctx.author

        if Path(f'facts/{filename.lower()}.txt').exists():
            await ctx.send(f'Fact list `{filename.lower()}` already exists.')
            return

        await ctx.send(f'Are you sure you want to create a new fact type named `{filename.lower()}`? (`y`)')
        message = await self.bot.wait_for('message', check=check_author)
        words = message.content.split()

        if words[0].lower() == 'y':
            with open(f'facts/{filename.lower()}.txt', 'w', encoding='utf-8') as file:
                file.write('')

        await ctx.send(f'Fact list `{filename.lower()}` created')

    async def get_fact(self, ctx, filename: str, min_time, *args):
        if len(args) > 0:
            if args[-1] == 'self_delete' and ctx.channel.type != 'private':
                await ctx.channel.delete_messages([ctx.message])

        facts, facts_str = strings.Files.get_facts(filename)
        last = len(facts)
        rand = random.randint(0, len(facts))
        if last == 1: rand = 0

        time_passed = datetime.now() - self.bot.last_fact
        minimum_seconds = min_time

        if len(args) > 1:
            if verifiers.integer(args[1], last):
                await self.get_specific(ctx, filename, args[1])
                return
            elif not verifiers.integer(args[1], last):
                await ctx.send(f'Please give a valid index for a fact. `(0-{last-1})`')
                return

        elif time_passed.seconds < minimum_seconds and not self.check_role(ctx, 'Staff'):
            logging.info('Ignored due to minimum time not reached.')
            await ctx.send(f'Please give me a little bit of time before asking again :) '
                           f'({minimum_seconds - time_passed.seconds}s)')
            return

        logging.info(f'Showing {filename.capitalize()} fact #{rand + 1}')
        logging.info(f'{facts[rand]}')

        await ctx.send(f'> {filename.capitalize()} Fact: {facts[rand]}')

        if filename in ['fun', 'hub']:
            self.bot.last_fact = datetime.now()

    @staticmethod
    async def get_specific(ctx, filename, index):
        facts, facts_str = strings.Files.get_facts(filename)
        await ctx.send(f'> {filename.capitalize()} Fact: {facts[int(index)]}')

    def check_role(self, ctx, role_name):
        guild: discord.Guild = discord.utils.get(self.bot.guilds, name=self.bot.guild_name)
        staff_role = discord.utils.get(guild.roles, name=role_name)

        if staff_role in ctx.author.roles:
            return True
        else:
            return False