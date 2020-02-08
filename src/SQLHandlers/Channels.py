import logging
from pathlib import Path
from sqlite3 import Error as sqlError


class Channels:

    def __init__(self, connection):
        self.connection = connection

    def create_row(self,
                   channel_id: int,
                   channel_name: str,
                   copy_target_id: int,
                   guild_id: int,
                   guild_name: str):

        if self.select_by_id(channel_id) is not None: return

        channel = (channel_id, channel_name, copy_target_id, guild_id, guild_name)

        sql = ''' 
        INSERT INTO channels(id, name, copy_target, guild_id, guild_name) 
        VALUES(?,?,?,?,?)
        '''

        cursor = self.connection.cursor()
        try:
            logging.info('Inserting ' + channel[1] + ' into guilds table')
            cursor.execute(sql, channel)
            self.connection.commit()
        except sqlError as e:
            logging.critical(e)

    def set_copy_target(self, channel_id, target_id):
        sql = ''' 
        UPDATE channels
        SET copy_target = ?
        WHERE id = ?
        '''
        values = (target_id, channel_id)

        try:
            cursor = self.connection.cursor()
            cursor.execute(sql, values)
            self.connection.commit()
        except sqlError as e:
            logging.critical(e)

    def select_by_id(self, id_: int):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM channels WHERE id=?', (id_,))
        return Channel(*cursor.fetchone())

    def select_by_name(self, name: str):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM channels WHERE name=?', (name,))
        return Channel(*cursor.fetchone())


class Channel:

    def __init__(self, id_, name, target_id, guild_id, guild_name):
        self.id_ = id_
        self.name = name
        self.target_id = target_id
        self.guild_id = guild_id
        self.guild_name = guild_name
