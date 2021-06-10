# databases file names
DATABASE_FILE_NAME = "001_schedule.db"
PATH_TO_FILES = './/schedules//'
SUBJECTS = ["001", 1002, 1003, 1005, 1006, 1009, 1010, 1011, 1015, 1016, 1017, 1018,
            1019, 1021, 1022, 100, 2007, 2012, 2013, 2014, 2020, 2023, 2024, 3001, 3002,
            3008]
DATABASES = [str(num) + "_schedule.db" for num in SUBJECTS]

# trials table parameters names:
BLOCK = "block"
STIM1 ="stim1"
STIM2 ="stim2"
FEEDBACK = "feedback"
CHOICE = "choice"
OUTCOME = "outcome"
CHOICE_TIME = "choice_time"
STIM_TIME = "stim_time"

# stimuli table parameters
NUMBER = "number"
REWARD = "reward"
RANK = "rank"
CONDITION = "condition"

# questionnaire table parameters
ANSWER_TIME = "answer_time"
ANSWER = "answer"

# feedback values
WITH_FEEDBACK = 1
NO_FEEDBACK = 0

# stimuli choice values
FIRST = 0
SECOND = 1

# stimuli success values
SUCCESS = 1
FAILURE = 0

# general
CONDITIONS = [1, 2, 3, 4]
CONDITIONS_DICT = {1: "3-2", 2: "6-2", 3: "3-4", 4: "6-4"}
PROBABILITIES = {1: "1", 2/3: "2/3", 1/3: "1/3", 0: "0"}
PROBABILITIES_MATTER = {1: "1", 2/3: "2/3", 1/3: "1/3"}
RANKS = [2, 1, 0]
RANKS_COLORS = {"2": "#b5edef", "1": "#feab98", "0": "#befe61"}
RANKS_MATTER = [2, 1]
HIGH_REWARD = "high reward"
LOW_REWARD = "low reward"
REWARDS_BY_RANK = {2: {HIGH_REWARD: 1, LOW_REWARD: 0.67},
                   1: {HIGH_REWARD: 0.67, LOW_REWARD: 0.33},
                   0: {HIGH_REWARD: 0.33, LOW_REWARD: 0}}
REWARDS_BY_RANK_ = {2: {1: HIGH_REWARD, 0.67: LOW_REWARD},
                    1: {0.67: HIGH_REWARD, 0.33: LOW_REWARD},
                    0: {0.33: HIGH_REWARD, 0: LOW_REWARD}}

# Short term learning across conditions
STIMULI_APPEARANCES_WITH_FEEDBACK = 62
APPEARANCES = "appearances"
RELATIVE_ACCURACY = "relative accuracy"
OBSERVED_ACCURACY = "observed accuracy"
TIME_DIFF = "time difference"
SLEEP_SCORE = "sleep score"
AVERAGE_ACCURACY = "average accuracy"