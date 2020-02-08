import logging
import sqlite3
from pathlib import Path
from sqlite3 import Error as sqlError

from SQLHandlers.Guilds import Guilds
from SQLHandlers.Channels import Channels


class SQLHandler:

    def __init__(self, root_path: Path,
                 db_filename: str = 'janets_thoughts.db',
                 tables_filename: str = 'tables'):

        self.filename: str = db_filename
        self.db_path: Path = root_path / db_filename
        self.tables_path: Path = root_path / 'src' / tables_filename

        self.connection = self._init_connection()
        self._init_tables()

        self.guilds = Guilds(self.connection)
        self.channels = Channels(self.connection)

    def _init_connection(self):

        connection = None
        try:
            connection = sqlite3.connect(str(self.db_path))
            logging.debug("Connection created to " + self.filename)
            logging.debug("SQLite version: " + sqlite3.version)
        except sqlError as e:
            logging.critical(e)

        return connection

    def _init_table(self, table_name, sql_table):
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql_table)
        except sqlError as e:
            logging.critical(table_name + ": ")
            logging.critical(e)

    def _init_tables(self):
        tables = []

        with open(str(self.tables_path), 'r') as tables_file:
            for line in tables_file:
                if line[:12] == 'CREATE TABLE':
                    tables.append('')
                    tables[-1] += line
                elif line == '\n': continue
                else: tables[-1] += line

        if self.connection is not None:
            for i, table in enumerate(tables):
                self._init_table("Table " + str(i), table)
        else:
            logging.critical("Error! Cannot create the database connection.")

    def close(self):
        logging.debug('Closing connection to database')
        self.connection.close()
