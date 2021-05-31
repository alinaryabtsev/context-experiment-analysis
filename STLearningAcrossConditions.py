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
                              hue=constants.RANK, ax=axs[i], sizes=(constants.LOW_REWARD,
                                                                    constants.HIGH_REWARD))
            for r in constants.RANKS:
                a = df.loc[df[constants.RANK] == str(r), constants.HIGH_REWARD].tolist()
                b = df.loc[df[constants.RANK] == str(r), constants.LOW_REWARD].tolist()
                ax.fill_between(df[constants.APPEARANCES].unique(), a, b,
                                facecolor=constants.RANKS_COLORS[str(r)], alpha=0.3)
            ax.set_title(f"relative accuracy of condition {condition} over trials")
            ax.set(ylim=(0, 1))
            ax.set(xlim=(1, None))
        plt.savefig(f"relative_accuracy_over_trials{'' if feedback else '_no_feedback'}.pdf")

    def observed_accuracy_over_each_trial_in_condition_ranks_ranges(self, feedback=True):
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
        fig.suptitle(f"Observed accuracy for possible conditions with"
                     f"{'' if feedback else ' no'} feedback")
        for i, condition in enumerate(constants.CONDITIONS):
            df = self.da.get_observed_accuracy_mean_per_condition_all_data_ranges(condition, feedback)
            if not feedback:
                ax = sns.lineplot(data=df, x=constants.APPEARANCES[:25],
                                  y=constants.OBSERVED_ACCURACY[:25],
                                  hue=constants.RANK, ax=axs[i], sizes=(constants.LOW_REWARD,
                                                                    constants.HIGH_REWARD))
            else:
                ax = sns.lineplot(data=df, x=constants.APPEARANCES, y=constants.OBSERVED_ACCURACY,
                                  hue=constants.RANK, ax=axs[i], ci="sd")
                ax = sns.lineplot(data=df, x=constants.APPEARANCES, y=constants.LOW_REWARD,
                                  dashes=[(5, 10), (5, 10)], hue=constants.RANK, ax=axs[i],
                                  sizes=(constants.LOW_REWARD, constants.HIGH_REWARD))
                ax = sns.lineplot(data=df, x=constants.APPEARANCES, y=constants.HIGH_REWARD,
                              hue=constants.RANK, ax=axs[i], sizes=(constants.LOW_REWARD,
                                                                    constants.HIGH_REWARD))
                ax.lines[0].set_linestyle("--")
                ax.lines[1].set_linestyle("--")
                ax.lines[2].set_linestyle("--")
            for r in constants.RANKS:
                a = df.loc[df[constants.RANK] == str(r), constants.HIGH_REWARD].tolist()
                b = df.loc[df[constants.RANK] == str(r), constants.LOW_REWARD].tolist()
                appearances = df[constants.APPEARANCES].unique()
                if not feedback:
                    a = a[:25]
                    b = b[:25]
                    appearances = appearances[:25]
                ax.fill_between(appearances, a, b,
                                facecolor=constants.RANKS_COLORS[str(r)], alpha=0.3, linewidth=1)
            axs[i].set_title(f"Observed accuracy of condition {condition} over trials")
            ax.set(ylim=(0, 1))
            ax.set(xlim=(1, None))
        plt.savefig(f"observed_accuracy_over_trials"
                    f"{'' if feedback else '_no_feedback'}_with_ranges.pdf")

    def observed_accuracy_over_each_trial_in_condition_ranks(self, feedback=True):
        """
        Generates graphs per each condition, where it takes the average of observed success rate
        of a stimuli from the given condition against how many times the stimuli appeared.

        X axis: Number of times stimuli was presented
        y axis: Observed Accuracy over these 72 trials

        Output: One line for Rank 1 (average all stimuli of rank 1), one line for rank 2 (all
        stimuli of rank 2), one line for rank 3 (all stimuli)
        :param feedback: plot the stimuli with feedback or those without
        """
        fig, axs = plt.subplots(nrows=4, figsize=(10, 30))
        fig.suptitle(f"Observed Accuracy for Possible Conditions With"
                     f"{'' if feedback else 'out'} feedback")
        for i, condition in enumerate(constants.CONDITIONS):
            df = self.da.get_observed_accuracy_mean_per_condition_all_data(condition, feedback)
            ax = sns.lineplot(data=df, x=constants.APPEARANCES, y=constants.OBSERVED_ACCURACY,
                              hue=constants.RANK, ax=axs[i])
            ax.set_title(f"observed accuracy of condition {condition} over trials")
            ax.set(ylim=(0, 1))
            ax.set(xlim=(1, None))
        plt.savefig(f"observed_accuracy_over_trials{'' if feedback else '_no_feedback'}.pdf")

    def relative_accuracy_within_time_differences(self, feedback=True):
        """
        Model within condition- accuracy (within feedback trials) but as a function of how many
        blocks they were learned apart

        X axis: Time Difference
        Y Axis:   1) Feedback accuracy of second session
                  2) No Feedback Accuracy (separate for each condition)

        :param feedback: with or without feedback
        """
        plt.title(f"relative accuracy within time differences across all conditions with"
                  f"{'' if feedback else ' no'} feedback")
        df = self.da.get_within_condition_accuracy_over_time_difference_all_conditions(feedback)
        sns.scatterplot(data=df, x=constants.TIME_DIFF, y=constants.RELATIVE_ACCURACY,
                        hue=constants.CONDITION,
                        palette=['green', 'orange', 'dodgerblue', 'red'], legend='full')
        plt.savefig(
            f"relative_accuracy_within_time_difference{'' if feedback else '_no_feedback'}.pdf")

    def observed_accuracy_within_time_differences(self, feedback=True):
        """
        Model within condition- by observed accuracy (within feedback trials) but as a function of
        how many blocks they were learned apart

        X axis: Time Difference
        Y Axis: With feedback observed accuracy of second session

        :param feedback: with or without feedback
        """
        plt.title(f"Observed accuracy within time differences across all conditions with"
                  f"{'' if feedback else ' no'} feedback")
        df = self.da.get_within_condition_observed_accuracy_over_time_difference_all_conditions(feedback)
        sns.scatterplot(data=df, x=constants.TIME_DIFF, y=constants.OBSERVED_ACCURACY,
                        hue=constants.CONDITION,
                        palette=['green', 'orange', 'dodgerblue', 'red'], legend='full')
        plt.savefig(
            f"observed_accuracy_within_time_difference{'' if feedback else '_no_feedback'}.pdf")

    def relative_accuracy_within_time_differences_distinct_plots(self, feedback=True):
        """
        plotting to distinct graphs relative accuracy (within feedback trials) but as a function of
        how many blocks they were learned apart.
        :param feedback: plot the data with feedback or without
        """
        fig, axs = plt.subplots(nrows=4, figsize=(10, 30))
        fig.suptitle(f"relative accuracy within time differences for possible conditions with"
                     f"{'' if feedback else ' no'} feedback")
        for i, condition in enumerate(constants.CONDITIONS):
            df = self.da.get_within_condition_accuracy_over_time_difference(condition, feedback)
            ax = sns.scatterplot(data=df, x=constants.TIME_DIFF, y=constants.RELATIVE_ACCURACY,
                                 ax=axs[i])
            ax.set_title(f"relative accuracy within time difference of condition {condition}")
            ax.set(ylim=(0, 1))
        plt.savefig(f"relative_accuracy_within_time_difference"
                    f"_per_condition{'' if feedback else '_no_feedback'}.pdf")