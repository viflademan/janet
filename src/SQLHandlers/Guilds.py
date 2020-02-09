import logging
from sqlite3 import Error as sqlError


class Guilds:

    def __init__(self, connection):
        self.connection = connection

    def create_row(self, id_: int, name: str):
        if self.select_by_id(id_) is not None: return

        row = (int(id_), name)

        sql = ''' 
        INSERT INTO guilds(id, name) 
        VALUES(?,?)
        '''

        try:
            logging.info('Inserting ' + row[1] + ' into guilds table')
            self.connection.cursor().execute(sql, row)
            self.connection.commit()
        except sqlError as e:
            logging.critical(e)

    def select_by_id(self, id_: int):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM guilds WHERE id=?', (id_,))
        result = cursor.fetchone()
        return Guild(*result)


class Guild:

    def __init__(self, id_: int, name: str):
        self.id_ = id_
        self.name = name
