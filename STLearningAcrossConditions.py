import matplotlib.pyplot as plt
from DataAnalyser import DataAnalyser

WITH_FEEDBACK = 1
NO_FEEDBACK = 0



class ShortTermLearningAcrossConditions:
    def __init__(self, db):
        self.da = DataAnalyser(db)

    def accuracy_over_time_condition(self, condition):
        trials = self.da.get_trials_filtered_by_condition_and_feedback(WITH_FEEDBACK, condition)
        # stimuli = self.da.get_stimuli()

        plt.plot()
        plt.title(f"Accuracy over time condition {condition}")
        plt.show()

    def reaction_time_over_accurate_choices_condition_1(self):
        trials = self.da.get_trials_filtered_by_condition_and_feedback(1, 1)
        chosen_right = DataAnalyser.filter_by_success(trials)



    def accuracy_over_time_by_rank_of_stimuli_condition_1(self):
        trials = self.da.get_trials_filtered_by_condition_and_feedback(1, 1)



