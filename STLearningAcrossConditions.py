import matplotlib.pyplot as plt
import seaborn as sns
from DataAnalyser import DataAnalyser
import constants
sns.set_style("darkgrid", {"axes.facecolor": ".9"})
sns.set_context("paper")


class ShortTermLearningAcrossConditions:
    def __init__(self, db):
        self.da = DataAnalyser(db)

    def accuracy_over_time_condition_per_probability(self, condition):
        fig, axs = plt.subplots(nrows=3, figsize=(6, 18))
        fig.suptitle(f"accuracy over time condition {condition} for possible probabilities")
        i = 0
        for probability, p in constants.PROBABILITIES_MATTER.items():
            df = self.da.get_trials_accuracy_by_condition_and_probability(condition, probability,
                                                                          constants.WITH_FEEDBACK)
            sns_plot = sns.scatterplot(x="blocks", y="success rate", data=df, ax=axs[i])
            axs[i].set_title(f"accuracy over time - probability {p}")
            i += 1
        plt.savefig(f"accuracy_over_time_by_probabilities_condition_{condition}.pdf")

    def accuracy_over_time_by_probabilities(self):
        for condition in constants.CONDITIONS:
            self.accuracy_over_time_condition_per_probability(condition)

    def accuracy_over_time_condition_per_rank(self, condition):
        fig, axs = plt.subplots(nrows=3, figsize=(6, 18))
        fig.suptitle(f"accuracy over time condition {condition} for possible ranks")
        for i, rank in enumerate(constants.RANKS_MATTER):
            df = self.da.get_trials_accuracy_by_condition_and_rank(condition, rank,
                                                                   constants.WITH_FEEDBACK)
            sns_plot = sns.scatterplot(x="blocks", y="success rate", data=df, ax=axs[i])
            axs[i].set_title(f"accuracy over time - rank {rank}")
        plt.savefig(f"accuracy_over_time_by_ranks_condition_{condition}.pdf")

    def accuracy_over_time_by_ranks(self):
        for condition in constants.CONDITIONS:
            self.accuracy_over_time_condition_per_rank(condition)

    def relative_accuracy_over_each_trial_in_condition_ranks(self, feedback=True):
        """
        Generates graphs per each condition, where it takes the average of success rate of a
        stimuli from the given condition against how many times the stimuli appeared.

        X axis: Number of times stimuli was presented
        y axis: Relative Accuracy over these 72 trials

        Output: One line for Rank 1 (average all stimuli of rank 1), one line for rank 2 (all
        stimuli of rank 2), one line for rank 3 (all stimuli)
        :param feedback: plot the stimuli with feedback or those without
        """
        fig, axs = plt.subplots(nrows=4, figsize=(10, 30))
        fig.suptitle(f"relative accuracy for possible conditions with"
                     f"{'' if feedback else ' no'} feedback")
        for i, condition in enumerate(constants.CONDITIONS):
            df = self.da.get_relative_accuracy_mean_per_condition_all_data(condition, feedback)
            ax = sns.lineplot(data=df, x=constants.APPEARANCES, y=constants.RELATIVE_ACCURACY,
                              hue=constants.RANK, ax=axs[i])
            ax.set_title(f"relative accuracy of condition {condition} over trials")
            ax.set(ylim=(0, 1))
            ax.set(xlim=(1, None))
        plt.savefig(f"relative_accuracy_over_trials{'' if feedback else '_no_feedback'}.pdf")

