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
        i = 0
        for rank in constants.RANKS_MATTER:
            df = self.da.get_trials_accuracy_by_condition_and_rank(condition, rank,
                                                                   constants.WITH_FEEDBACK)
            sns_plot = sns.scatterplot(x="blocks", y="success rate", data=df, ax=axs[i])
            axs[i].set_title(f"accuracy over time - rank {rank}")
            i += 1
        plt.savefig(f"accuracy_over_time_by_ranks_condition_{condition}.pdf")

    def accuracy_over_time_by_ranks(self):
        for condition in constants.CONDITIONS:
            self.accuracy_over_time_condition_per_rank(condition)


