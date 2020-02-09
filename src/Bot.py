# BotClient.py
import json
import logging
import datetime
import discord
from discord.ext import commands
from pathlib import Path

from cogs.BaseCog import BaseCog
from cogs.FactsCog import FactsCog
from cogs.ServerManagement import ServerManagement

from SQLHandlers._SQLHandler import SQLHandler


class Bot(commands.Bot):

    def __init__(self, token, guild_name):
        commands.Bot.__init__(self, ';')

        self.token = token
        self.guild_name = guild_name

        self.root = Path.cwd().parent
        self.db = SQLHandler(self.root)
        self.init_datetime = datetime.datetime.now()
        self.last_fact = datetime.datetime.min

        self.add_cog(BaseCog(self))
        self.add_cog(FactsCog(self))
        self.add_cog(ServerManagement(self))

        self.run(token, bot=True, reconnect=True)

    async def on_ready(self):
        self.init_db()
        logging.info(f' --------------- Bot started!')
        logging.info(f'{self.user} has connected to {self.guild_name}')
        # todo display channels
        for channel in self.db.channels.select_if_target_id():
            pass
        # logging.info(f'Watching: {self.get_read_channel_list()}')
        # logging.info(f'Copying to {self.get_copy_channel_list()}')

    def init_db(self):
        for guild in self.guilds:
            self.db.guilds.create_row(guild.id, guild.name)
            for channel in guild.channels:
                if isinstance(channel, discord.TextChannel):
                    self.db.channels.create_row(channel.id, channel.name, None, guild.id, guild.name)

        sfw = 361137896578744320
        nsfw = 353003422284513280
        art_gallery = 612039801620660243
        void = 640279442878627850
        void_gallery = 675576621079592970

        self.db.channels.set_copy_target(sfw,  art_gallery)  # sfw copies to gallery
        self.db.channels.set_copy_target(nsfw, art_gallery)  # nsfw copies to gallery
        self.db.channels.set_copy_target(void, void_gallery)  # void to void_gallery

    async def on_message(self, message: discord.message):
        if message.author == self.user: return  # if message is from janet, prevents infinite loop
        channel = self.db.channels.select_by_id(message.channel.id)

        # check if message has attachments
        if len(message.attachments) > 0 and channel.target_id is not None:
            for attachment in message.attachments:

                dimensions = str(attachment.width) + ' x ' + str(attachment.height)
                size = self.get_size(attachment.size)

                embed = discord.Embed(color=0x31eb31)
                logging.info('---------------')
                embed.add_field(name="Artist", value=message.author.display_name, inline=True)
                logging.info('Artist: ' + message.author.display_name)
                embed.set_image(url=attachment.url)
                logging.info('URL: ' + attachment.url)
                embed.add_field(name="Dimensions", value=dimensions, inline=True)
                logging.info('Dimensions: ' + dimensions)
                embed.add_field(name="Size", value=size, inline=True)
                logging.info('Size: ' + str(size))
                if len(message.content) > 0:
                    embed.add_field(name="Message", value=message.content, inline=False)
                    logging.info('Message: ' + message.content)
                logging.info('Source: ' + channel.name)
                logging.info('Destination: ' + self.get_channel_name(channel.target_id))

                await self.send_message(channel.target_id, None, embed)

        await self.process_commands(message)

    async def send_message(self, channel_id, content=None, embed=None):
        guild = discord.utils.get(self.guilds, name=self.guild_name)
        copy_channel = discord.utils.get(guild.text_channels, id=channel_id)

        await copy_channel.send(content, embed=embed)

    def get_channel_name(self, channel_id):
        guild = discord.utils.get(self.guilds, name=self.guild_name)
        channel = discord.utils.get(guild.text_channels, id=channel_id)

        return channel.name

    def get_read_channel_list(self):
        read_channels = str()

        for channel_id in self.read_channel_ids.values():
            read_channels += f'#{self.get_channel_name(channel_id)} '

        return read_channels

    def get_copy_channel_list(self):
        copy_channels = str()

        for channel_id in self.copy_channel_ids.values():
            copy_channels += f'#{self.get_channel_name(channel_id)} '

        return copy_channels

    def write_channels(self):
        guild = discord.utils.get(self.guilds, name=self.guild_name)
        text = str()

        with open('channels.txt', mode='w', encoding='utf-8') as out_file:
            for channel in guild.text_channels:
                line = f'{channel.name}: {channel.id},\n'

                print(line)
                text += line

            out_file.write(text)

    def get_size(self, size_raw, places=2):
        if size_raw > 2 ** 30:
            size = size_raw / 2 ** 30
            ext = ' GB'
        elif size_raw > 2 ** 20:
            size = size_raw / 2 ** 20
            ext = ' MB'
        else:
            size = size_raw / 2 ** 10
            ext = ' KB'

        return str(round(size, places)) + ext

