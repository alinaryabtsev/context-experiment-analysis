# databases file names
DATABASE_FILE_NAME = "001_schedule.db"
PATH_TO_FILES = './/schedules//'
DATABASES = ["2_schedule.db", "1003_schedule.db", "1006_schedule.db",
             "1010_schedule.db", "1018_schedule.db", "1019_schedule.db", "1021_schedule.db",
             "1022_schedule.db"]


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
PROBABILITIES = {1: "1", 2/3: "2/3", 1/3: "1/3", 0: "0"}
PROBABILITIES_MATTER = {1: "1", 2/3: "2/3", 1/3: "1/3"}
RANKS = [2, 1, 0]
RANKS_MATTER = [2, 1]

# Short term learning across conditions
STIMULI_APPEARANCES_WITH_FEEDBACK = 62
APPEARANCES = "appearances"
RELATIVE_ACCURACY = "relative accuracy"
