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

    async def on_message(self, message: discord.message):
        if message.author == self.user: return  # if message is from janet, prevents infinite loop

        # check if message has attachments
        # check if message in watched channels
        elif len(message.attachments) > 0 and message.channel.id in self.read_channel_ids.values():
            for attachment in message.attachments:

                dimensions = str(attachment.width) + ' x ' + str(attachment.height)
                size = self.get_size(attachment.size)

                embed = discord.Embed(color=0x31eb31)
                embed.set_image(url=attachment.url)
                embed.add_field(name="Artist", value=message.author.display_name, inline=True)
                embed.add_field(name="Dimensions", value=dimensions, inline=True)
                embed.add_field(name="Size", value=size, inline=True)
                if len(message.content) > 0:
                    embed.add_field(name="Message", value=message.content, inline=False)

                for channel_id in self.copy_channel_ids.values():
                    await self.send_message(channel_id, None, embed)

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