# BotClient.py
import logging
import datetime
import discord
from discord.ext import commands
from cogs.BaseCog import BaseCog
from cogs.FactsCog import FactsCog
from cogs.ServerManagement import ServerManagement

channels = {
    'sfw_other_artwork': 361137896578744320,
    'nsfw_artwork': 353003422284513280,
    'the_void': 640279442878627850,
    'art_gallery': 612039801620660243,
    'content_requests': 353367822157479937,
    'edit_log': 672313178197196821,
    'delete_log': 673015035576188948
}


class Bot(commands.Bot):

    def __init__(self, token, guild_name):
        commands.Bot.__init__(self, ';')

        self.token = token
        self.guild_name = guild_name

        self.read_channel_ids = {
            'sfw': 361137896578744320,
            'nsfw': 353003422284513280
        }
        self.copy_channel_ids = {
            'gallery': 612039801620660243
        }

        self.init_datetime = datetime.datetime.now()
        self.reposts = 0
        self.embeds = 0

        self.last_fact = datetime.datetime.min

        self.add_cog(BaseCog(self))
        self.add_cog(FactsCog(self))
        self.add_cog(ServerManagement(self))

        self.run(token, bot=True, reconnect=True)

    async def on_ready(self):
        read_channels = str()
        copy_channels = str()

        for channel_id in self.read_channel_ids.values():
            read_channels += f'#{self.get_channel_name(channel_id)} '

        for channel_id in self.copy_channel_ids.values():
            copy_channels += f'#{self.get_channel_name(channel_id)} '

        logging.info(f' --------------- Bot started!')
        logging.info(f'{self.user} has connected to {self.guild_name}')
        logging.info(f'Watching: {read_channels}')
        logging.info(f'Copying to {copy_channels}')

    """
    async def on_message_delete(self, message: discord.message):
        if message.author == self.user: return  # if message is from janet, prevents infinite loop
        if message.channel.guild.name != 'Developers Hub': return

        embed = discord.Embed(title=f'Message deleted in #{message.channel.name}',
                              color=0xff0000)  # red

        nick = message.author.nick if message.author.nick is not None else str(message.author)[:-5]
        embed.set_author(name=nick, icon_url=message.author.avatar_url)

        embed.add_field(name='Author Username', value=message.author, inline=True)
        embed.add_field(name='Author ID', value=message.author.id, inline=True)

        created_at = message.created_at.strftime('%H:%M GMT on %d %b \'%y ')
        embed.add_field(name="Created at", value=created_at, inline=False)

        embed.add_field(name="Message Content", value=message.content, inline=False)

        embed.timestamp = datetime.datetime.now(datetime.timezone.utc)

        await self.send_message(channels['delete_log'], content='', embed=embed)
        logging.info(f'A message by {message.author.nick} in #{message.channel.name} was deleted')

    async def on_message_edit(self, before: discord.message, after: discord.message):
        if before.author == self.user: return  # if message is from janet, prevents infinite loop
        if before.channel.guild.name != 'Developers Hub': return
        if before.content == after.content: return

        embed = discord.Embed(title=f'Message edited in #{before.channel.name}',
                              color=0x53ff00)  # green

        nick = before.author.nick if before.author.nick is not None else str(before.author)[:-5]

        embed.set_author(name=nick, icon_url=before.author.avatar_url)
        embed.add_field(name='Username', value=before.author, inline=True)
        embed.add_field(name='Discord ID', value=before.author.id, inline=True)
        embed.add_field(name="Before", value=before.content, inline=False)
        embed.add_field(name="After", value=after.content, inline=False)

        embed.timestamp = datetime.datetime.now(datetime.timezone.utc)

        await self.send_message(channels['edit_log'], content='\u200b', embed=embed)
        logging.info(f'{before.author.nick} edited a message in #{before.channel.name}')
    """

    async def on_message(self, message: discord.message):
        if message.author == self.user: return  # if message is from janet, prevents infinite loop

        # check if message has attachments
        # check if message in watched channels
        if len(message.attachments) > 0 and message.channel.id in self.read_channel_ids.values():
            for attachment in message.attachments:
                self.reposts += 1
                self.embeds += 1

                embed = discord.Embed().set_image(url=attachment.url)

                content = 'Posted by **' + message.author.display_name + '**'
                if len(message.content) > 0:
                    content += '\n> ' + message.content

                logging.info('-----------------')
                logging.info(f'Filename: {attachment.filename}')
                logging.info(f'Poster: {message.author.display_name}')
                if len(message.content) > 0:
                    logging.info(f'Message: {message.content}')

                for channel_id in self.copy_channel_ids.values():
                    await self.send_message(channel_id, content, embed)

        await self.process_commands(message)

    async def send_message(self, channel_id, content=None, embed=None):
        guild = discord.utils.get(self.guilds, name=self.guild_name)
        copy_channel = discord.utils.get(guild.text_channels, id=channel_id)

        await copy_channel.send(content, embed=embed)

    def get_channel_name(self, channel_id):
        guild = discord.utils.get(self.guilds, name=self.guild_name)
        channel = discord.utils.get(guild.text_channels, id=channel_id)

        return channel.name

    def write_channels(self):
        guild = discord.utils.get(self.guilds, name=self.guild_name)
        text = str()

        with open('channels.txt', mode='w', encoding='utf-8') as out_file:
            for channel in guild.text_channels:
                text += f'{channel.name}: {channel.id},\n'

            out_file.write(text)

