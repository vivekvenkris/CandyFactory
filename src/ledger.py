import sqlite3
from sqlite3 import Error
import os
from log import Logger
import threading
from status_manager import StatusManager
from pathlib import Path


class Ledger(object):

    lock = threading.Lock()

    __instance = None
    @staticmethod
    def getInstance():
        """ Static access method. """
        if Ledger.__instance == None:
            Ledger()
        return Ledger.__instance

    @staticmethod
    def create_connection(db_file, logger):
        """ create a database connection to a SQLite database """
        conn = None
        try:
               
            conn = sqlite3.connect(db_file, check_same_thread=False)
            logger.info(sqlite3.version)

            return conn
        except Error as e:            
            logger.fatal(e)

    @staticmethod
    def transact_with_db(conn, sql, logger):
        """ create a table from the create_table_sql statement
        :param conn: Connection object
        :param sql: an SQL statement
        :return:
        """
        try:
            logger.debug(sql)
            Ledger.lock.acquire();
            c = conn.cursor()
            return_value = c.execute(sql)
            conn.commit()
            Ledger.lock.release()
            return return_value
        except Error as e:
            print("error")
            logger.fatal(e)


    def  __init__(self, name):

        """
        init ledger
        :param name: name of ledger
        :return:
        """

        if Ledger.__instance != None:
            raise Exception("This class is a singleton! use Ledger.getInstance()")
        else:
            Ledger.__instance = self

        self.logger = Logger.getInstance().logger

        self.conn = Ledger.create_connection(name, self.logger)

        self.status_manager = StatusManager.getInstance()

        create_processing_status = "CREATE TABLE IF NOT EXISTS processing_status(name varchar, status varchar NOT NULL, search_type varchar NOT NULL, PRIMARY KEY (name, search_type));"
        Ledger.transact_with_db(self.conn, create_processing_status, self.logger)

    def __del__(self):
        """
        delete ledger
        :return:
        """

        if self.conn:
            self.conn.close()

    def add_to_ledger(self, beam_name, search_type="DEF"):
        insert_processing_status="INSERT INTO processing_status(name, search_type, status) values(\"{}\", \"{}\",0)".format(beam_name, search_type)
        Ledger.transact_with_db(self.conn, insert_processing_status, self.logger)

    def update_status(self, beam_name, status, search_type="DEF"):
        update_processing_status="UPDATE processing_status SET status = {} WHERE name = \"{}\" AND search_type = \"{}\"".format(status, beam_name, search_type)
        Ledger.transact_with_db(self.conn, update_processing_status, self.logger)

    def has_beam(self, beam_name, search_type="DEF"):
        select_processing_status="SELECT * FROM processing_status WHERE name = \"{}\" AND search_type = \"{}\"".format(beam_name, search_type)
        ret = Ledger.transact_with_db(self.conn, select_processing_status, self.logger).fetchall()
        return len(ret) > 0

    def get_status(self, beam_name, search_type="DEF"):
        select_processing_status="SELECT status FROM processing_status WHERE name = \"{}\" AND search_type = \"{}\"".format(beam_name, search_type)
        ret = Ledger.transact_with_db(self.conn, select_processing_status, self.logger).fetchall()
        return int(ret[0][0])

    def get_beams_for_status(self, status, search_type="DEF"):
        select_beams="SELECT name FROM processing_status WHERE status = \"{}\" AND search_type = \"{}\"".format(status, search_type)
        ret = Ledger.transact_with_db(self.conn, select_beams, self.logger).fetchall()
        ret = [x[0] for x in ret]
        return ret 


    def get_ledger_table(self):
        table_query = "SELECT * FROM processing_status"
        ret = Ledger.transact_with_db(self.conn, table_query, self.logger).fetchall()
        return ret

    def get_pretty_ledger_table(self):

        s = ""
        default = table_array[ table_array[:,2] == "DEF" ]
        acc = table_array[ table_array[:,2] == self.status_manager.SEARCH_TYPE_ACC ]
        zero_acc = table_array[ table_array[:,2] == self.status_manager.SEARCH_TYPE_ZERO_ACC ]
        segmented = table_array[ table_array[:,2] == self.status_manager.SEARCH_TYPE_SEGMENTED ]




    def get_num_running_beams(self):
        select_processing_status="SELECT count(*) FROM processing_status where status >= {}".format(self.status_manager.RSYNC_TO_PROCESSING)
        ret = Ledger.transact_with_db(self.conn, select_processing_status, self.logger).fetchall()
        return ret[0][0]





if __name__ == '__main__':
    ledger = Ledger()