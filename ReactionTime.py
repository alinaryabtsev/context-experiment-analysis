from math import floor

import matplotlib.pyplot as plt
import seaborn as sns
from DataAnalyser import DataAnalyser
import constants
sns.set_style("darkgrid", {"axes.facecolor": ".9"})
sns.set_context("paper")
sns.set(rc={'figure.figsize': (11.7, 8.27)})


class ReactionTime:
    def __init__(self, db):
        self.da = DataAnalyser(db)

    def mean_reaction_time_correct_vs_incorrect_all_blocks(self):
        reaction_times = self.da.get_reaction_time_mean_all_experiment()
        sns_plot = sns.barplot(x="blocks", y="RT mean", data=reaction_times,
                               hue="answer correctness")
        sns_plot.set_title("Reaction times mean across blocks")
        plt.savefig(f"mean_reaction_time_over_all_blocks.pdf")

    def mean_reaction_time_correct_vs_incorrect_per_condition(self):
        fig, axs = plt.subplots(2, 2, figsize=(14, 12))
        fig.suptitle("Reaction time means across all conditions")
        ind = {0: (0, 0), 1: (0, 1), 2: (1, 0), 3: (1, 1)}
        for i, condition in enumerate(constants.CONDITIONS):
            reaction_times = self.da.get_reaction_time_mean_by_condition(condition=condition)
            sns_plot = sns.barplot(x="blocks", y="RT mean", data=reaction_times,
                                   hue="answer correctness", ax=axs[ind[i][0]][ind[i][1]])
            sns_plot.set_title(f"Reaction times mean across condition {condition}")
        fig.savefig(f"mean_reaction_time_over_all_blocks_by_conditions.pdf")

