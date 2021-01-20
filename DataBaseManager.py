import sqlite3
import sys
import os

REWARD = "reward"
RANK = "rank"
CONDITION = "condition"
STIM1 ="stim1"
STIM2 ="stim2"
FEEDBACK = "feedback"
CHOICE = "choice"
OUTCOME = "outcome"
CHOICE_TIME = "choice_time"
STIM_TIME = "stim_time"

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
        self.curr.execute(SQL_QUERY_GET_ALL_STIMULI)
        stimuli_data = self.curr.fetchall()
        stimuli = dict()
        for row in stimuli_data:
            stimuli[row[0]] = {
                REWARD: row[1],
                RANK: row[2],
                CONDITION: row[3]
            }
        return stimuli

    def get_all_trials_with_stimuli(self):
        self.curr.execute(SQL_QUERY_GET_TRIALS)
        trials_data = self.curr.fetchall()
        trials = dict()
        for row in trials_data:
            if row[0] not in trials:
                trials[row[0]] = []
            data = {
                STIM1: row[1],
                STIM2: row[2],
                FEEDBACK: row[3],
                CHOICE: row[4],
                OUTCOME: row[5],
                CHOICE_TIME: row[6],
                STIM_TIME: row[7]
            }
            trials[row[0]].append(data)
        return trials
