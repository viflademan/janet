import logging
from sqlite3 import Error as sqlError


class Channels:

    def __init__(self, connection):
        self.connection = connection

    def create_row(self,
                   channel_id: int,
                   channel_name: str,
                   target_id: int,
                   guild_id: int,
                   guild_name: str):

        if self.select_by_id(channel_id) is not None: return

        row = (channel_id, channel_name, target_id, guild_id)

        sql = ''' 
        INSERT INTO channels(id, name, copy_target, guild_id) 
        VALUES(?,?,?,?)
        '''

        try:
            logging.info('Inserting ' + row[1] + ' into guilds table')
            self.connection.cursor().execute(sql, row)
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

    def select_if_target_id(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute('SELECT * FROM channels WHERE target_id IS NOT NULL')
            rows = cursor.fetchall()
        except sqlError as e:
            logging.critical(e)
            return None

        channels = list()
        for row in rows:
            channels.append(Channel(*row))

        return channels


class Channel:

    def __init__(self, id_, name, target_id, guild_id):
        self.id_ = id_
        self.name = name
        self.target_id = target_id
        self.guild_id = guild_id

    @property
    def target_name(self):

        return name