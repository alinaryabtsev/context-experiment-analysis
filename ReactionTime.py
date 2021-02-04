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
                               hue="correct answer")
        sns_plot.set_title("Reaction times mean across blocks")
        plt.savefig(f"mean_reaction_time_over_all_blocks.pdf")

