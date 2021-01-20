import sqlite3
import sys
import os
import constants

SQL_QUERY_GET_ALL_STIMULI = "SELECT number, reward, rank, condition FROM stimuli " \
                            "WHERE condition >= 1 AND condition <= 4"
SQL_QUERY_GET_TRIALS = "SELECT block, stim1, stim2, feedback, choice, outcome, choice_time, " \
                       "stim_time FROM trials WHERE block > 12 AND block < 1000"


class DataBaseManager:
    def __init__(self, file_path):
        if file_path not in os.listdir(os.getcwd()):
            print(f"No database file have been found. Please make sure the data base file is "
                  f"named as {file_path} and can be found where the script is.")
            sys.exit()
        self.conn = sqlite3.connect(file_path)
        self.curr = self.conn.cursor()

    def get_all_stimuli(self):
        """
        :return: a dictionary representing stimuli table as follows:
                { stimuli number : { REWARD: reward value of stimuli,
                                     RANK: rank value of the stimuli,
                                     CONDITION: condition the stimuli relates to }
                   .... }
        """
        self.curr.execute(SQL_QUERY_GET_ALL_STIMULI)
        stimuli_data = self.curr.fetchall()
        stimuli = dict()
        for row in stimuli_data:
            stimuli[row[0]] = {
                constants.REWARD: row[1],
                constants.RANK: row[2],
                constants.CONDITION: row[3]
            }
        return stimuli

    def get_all_trials_with_stimuli(self):
        """
        :return: a dictionary representing trials table as follows:
                { block number: [ {STIM1: stimuli 1 number, STIM2: stimuli 2 number,
                                   FEEDBACK: 0/1, CHOICE: 0/1 (first/second stimuli), OUTCOME: 0/1,
                                   CHOICE_TIME: UTC time when chosen, STIM_TIME: UTC time when
                                   appeared} ...]
                .... }
        """
        self.curr.execute(SQL_QUERY_GET_TRIALS)
        trials_data = self.curr.fetchall()
        trials = dict()
        for row in trials_data:
            if row[0] not in trials:
                trials[row[0]] = []
            data = {
                constants.STIM1: row[1],
                constants.STIM2: row[2],
                constants.FEEDBACK: row[3],
                constants.CHOICE: row[4],
                constants.OUTCOME: row[5],
                constants.CHOICE_TIME: row[6],
                constants.STIM_TIME: row[7]
            }
            trials[row[0]].append(data)
        return trials
