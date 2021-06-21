import sqlite3
from sqlite3 import Error
import os
from log import Logger


def create_connection(db_file, logger):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        logger.info(sqlite3.version)
        return conn
    except Error as e:
        logger.fatal(e)

def transact_with_db(conn, create_table_sql, logger):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        return c.execute(create_table_sql)
    except Error as e:
        logger.fatal(e)



class Ledger(object):

    __instance = None
    @staticmethod
    def getInstance():
        """ Static access method. """
        if Ledger.__instance == None:
            Ledger()
        return Ledger.__instance


    def  __init__(self, name):

        if Ledger.__instance != None:
            raise Exception("This class is a singleton! use Ledger.getInstance()")
        else:
            Ledger.__instance = self

        self.logger = Logger.getInstance().logger

        self.conn = create_connection(name, self.logger)
        create_processing_status = "CREATE TABLE IF NOT EXISTS processing_status(name varchar, status varchar NOT NULL, search_type varchar NOT NULL, PRIMARY KEY (name));"
        transact_with_db(self.conn, create_processing_status, self.logger)

    def add_to_ledger(beam_name, type=0):
        insert_processing_status="INSERT INTO processing_status(name, search_type, status) values({}, {},0)".format(beam_name, search_type)
        transact_with_db(self.conn, create_processing_status, self.logger)

    def update_status(beam_name, status, type=0):
        update_processing_status="UPDATE processing_status SET status = {} WHERE name = {} AND search_type = {}".format(status, beam_name, search_type)
        transact_with_db(self.conn, create_processing_status, self.logger)

    def has_beam(beam_name, type=0):
        select_processing_status="SELECT * FROM processing_status WHERE name = {} AND search_type = {}".format(beam_name, search_type)
        ret = transact_with_db(self.conn, select_processing_status, self.logger)
        return len(ret) > 0

    def get_status(beam_name, type=0):
        select_processing_status="SELECT status FROM processing_status WHERE name = {} AND search_type = {}".format(beam_name, search_type)
        ret = transact_with_db(self.conn, select_processing_status, self.logger)
        return ret[0]

    def get_num_running_beams():
        select_processing_status="SELECT count(*) FROM processing_status WHERE name = {}".format(beam_name)
        ret = transact_with_db(self.conn, select_processing_status, self.logger)
        return lret[0]



if __name__ == '__main__':
    ledger = Ledger()