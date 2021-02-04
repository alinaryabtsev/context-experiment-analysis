import matplotlib.pyplot as plt
import seaborn as sns
from DataAnalyser import DataAnalyser
import constants
sns.set_style("darkgrid", {"axes.facecolor": ".9"})
sns.set_context("paper")


class ReactionTime:
    def __init__(self, db):
        self.da = DataAnalyser(db)

    def mean_reaction_time_correct_vs_incorrect(self, condition):
        correct_trials_times = self.da.get_reaction_times_of_correct_or_incorrect_trials(True)

