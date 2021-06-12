import DataBaseManager
from STLearningAcrossConditions import ShortTermLearningAcrossConditions
from ReactionTime import ReactionTime
import constants


def main():
    databases = [constants.PATH_TO_FILES + filename for filename in constants.DATABASES]
    # databases = [constants.DATABASE_FILE_NAME]
    db = DataBaseManager.DataBaseManager(*databases)
    stl_analyser = ShortTermLearningAcrossConditions(db)
    # stl_analyser.accuracy_over_time_by_probabilities()
    # stl_analyser.accuracy_over_time_by_ranks()
    # rt_analyser = ReactionTime(db)
    # rt_analyser.mean_reaction_time_correct_vs_incorrect_all_blocks()
    # rt_analyser.mean_reaction_time_correct_vs_incorrect_per_condition()

    # stl_analyser.observed_accuracy_over_each_trial_in_condition_ranks()
    # stl_analyser.observed_accuracy_over_each_trial_in_condition_ranks(False)

    # stl_analyser.observed_accuracy_over_each_trial_avergaed(True)
    # stl_analyser.observed_accuracy_over_each_trial_avergaed(False)

    # stl_analyser.observed_accuracy_over_each_trial_in_condition_ranks_ranges(True)
    # stl_analyser.observed_accuracy_over_each_trial_in_condition_ranks_ranges(False)

    stl_analyser.observed_accuracy_over_each_trial_in_condition_ranks_ranges_averaged(True)
    stl_analyser.observed_accuracy_over_each_trial_in_condition_ranks_ranges_averaged(False)

    # stl_analyser.relative_accuracy_within_time_differences()
    # stl_analyser.observed_accuracy_within_time_differences_conditions_2_4(True)
    # stl_analyser.observed_accuracy_within_time_differences_conditions_2_4(False)

    # stl_analyser.average_accuracy_over_sleep_quality()



if __name__ == '__main__':
    main()
