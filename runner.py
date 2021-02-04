import DataBaseManager
from STLearningAcrossConditions import ShortTermLearningAcrossConditions
from ReactionTime import ReactionTime

DATABASE_FILE_NAME = "001_schedule.db"


def main():
    db = DataBaseManager.DataBaseManager(DATABASE_FILE_NAME)
    stl_analyser = ShortTermLearningAcrossConditions(db)
    stl_analyser.accuracy_over_time_by_probabilities()
    stl_analyser.accuracy_over_time_by_ranks()
    # rt_analyser = ReactionTime(db)
    # rt_analyser.mean_reaction_time_correct_vs_incorrect_all_blocks()
    # rt_analyser.mean_reaction_time_correct_vs_incorrect_per_condition()


if __name__ == '__main__':
    main()
