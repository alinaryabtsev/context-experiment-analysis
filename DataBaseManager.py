import sqlite3
import sys
import os
import pandas as pd
import constants

SQL_QUERY_GET_ALL_STIMULI = "SELECT number, reward, rank, condition FROM stimuli " \
                            "WHERE condition >= 1 AND condition <= 4"
SQL_QUERY_GET_TRIALS = "SELECT block, stim1, stim2, feedback, choice, outcome, choice_time, " \
                       "stim_time FROM trials WHERE block > 12 AND block < 99"


class DataBaseManager:
    """
    This module manages data extraction from DB file
    """
    def __init__(self, *args):
        """
        Initializes databases connections
        :param args: databases names to connect with
        """
        self.conns = []
        for file_path in args:
            if not os.path.exists(file_path):
                print(f"No database file have been found. Please make sure the data base file is "
                      f"named as {file_path} and can be found where the script is.")
            else:
                self.conns.append(sqlite3.connect(file_path))
        if not len(self.conns):
            sys.exit()

    def get_all_stimuli(self):
        """
        :return: a list of data frames according to given databases.
                 Each data frame contains stimuli table including stimuli number, reward value of
                 stimuli, stimuli's rank, stimuli's condition.
        """
        return [pd.read_sql_query(SQL_QUERY_GET_ALL_STIMULI, conn) for conn in self.conns]

    def get_all_trials_with_stimuli(self):
        """
        :return: A list of data frames according to given databases.
                Each data frame of trials including block number, stimuli 1 number, stimuli 2 number,
                feedback value: 0/1, choice value: 0/1 (first/second stimuli), outcome value: 0/1,
                choice time: UTC timestamp when chosen, stimuli time: UTC timestamp when appeared
        """
        return [pd.read_sql_query(SQL_QUERY_GET_TRIALS, conn) for conn in self.conns]

