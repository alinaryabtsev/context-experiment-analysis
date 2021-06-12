import math

import matplotlib.pyplot as plt
import seaborn as sns
from DataAnalyser import DataAnalyser
import constants
import pandas as pd

sns.set_style("darkgrid", {"axes.facecolor": ".9"})
sns.set_context("paper")


class ShortTermLearningAcrossConditions:
    def __init__(self, db):
        self.da = DataAnalyser(db)

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
        fig, axs = plt.subplots(nrows=2, ncols=2)
        # fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(10, 30))
        fig.suptitle(f"Observed Accuracy for Possible Conditions With{'' if feedback else 'out'} feedback")
        for i, condition in enumerate(constants.CONDITIONS):
            df = self.da.get_observed_accuracy_mean_per_condition_all_data_ranges(condition, feedback)
            ax = sns.lineplot(data=df, x=constants.APPEARANCES, y=constants.OBSERVED_ACCURACY,
                              hue=constants.RANK, ax=axs[math.floor(i/2)][i % 2])
            ax.set_title(f"Observed accuracy of condition {constants.CONDITIONS_DICT[condition]} over trials")
            ax.legend(constants.RANK_LABELS)
            ax.set(ylim=(0, 1))
            ax.set(xlim=(1, None))
        fig.tight_layout()
        plt.savefig(f"observed_accuracy_over_trials{'' if feedback else '_no_feedback'}.pdf")

    def observed_accuracy_over_each_trial_avergaed(self, feedback=True):
        """
        Generates graphs per each condition, where it takes the average of observed success rate
        of a stimuli from the given condition against how many times the stimuli appeared.

        X axis: Number of times stimuli was presented
        y axis: Observed Accuracy over these 72 trials

        Output: One line for Rank 1 (average all stimuli of rank 1), one line for rank 2 (all
        stimuli of rank 2), one line for rank 3 (all stimuli)
        :param feedback: plot the stimuli with feedback or those without
        """
        conditions = []
        for condition in constants.CONDITIONS:
            conditions.append(self.da.get_observed_accuracy_mean_per_condition_all_data_ranges(condition, feedback))
        df = pd.concat(conditions, axis=0, ignore_index=True)
        ax = sns.lineplot(data=df, x=constants.APPEARANCES, y=constants.OBSERVED_ACCURACY,
                          hue=constants.RANK)
        plt.title("Observed accuracy over trials averaged")
        ax.legend(constants.RANK_LABELS)
        ax.set(ylim=(0, 1))
        ax.set(xlim=(1, None))
        plt.savefig(f"observed_accuracy_over_trials{'' if feedback else '_no_feedback'}.pdf")

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
        fig, axs = plt.subplots(nrows=2, ncols=2)
        fig.suptitle(f"Observed accuracy for possible conditions with{'' if feedback else ' no'} feedback")
        for i, condition in enumerate(constants.CONDITIONS):
            df = self.da.get_observed_accuracy_mean_per_condition_all_data_ranges(condition, feedback)
            ax = sns.lineplot(data=df, x=constants.APPEARANCES, y=constants.LOW_REWARD, ax=axs[math.floor(i/2)][i % 2],
                              hue=constants.RANK, sizes=(constants.LOW_REWARD, constants.HIGH_REWARD))
            ax = sns.lineplot(data=df, x=constants.APPEARANCES, y=constants.HIGH_REWARD, ax=axs[math.floor(i/2)][i % 2],
                              hue=constants.RANK, sizes=(constants.LOW_REWARD, constants.HIGH_REWARD))
            for k in range(3):
                ax.lines[k].set_linestyle("--")
            ax.legend(constants.RANK_REWARD_LABELS)
            ax.set(xlabel=constants.APPEARANCES, ylabel=constants.OBSERVED_ACCURACY)
            ax.set(ylim=(0, 1))
            ax.set(xlim=(1, None))
            axs[math.floor(i/2)][i % 2].set_title(f"Observed accuracy of condition {constants.CONDITIONS_DICT[condition]} over trials")
            fig.tight_layout()
        plt.savefig(f"observed_accuracy_over_trials{'' if feedback else '_no_feedback'}_with_ranges.pdf")

    def observed_accuracy_over_each_trial_in_condition_ranks_ranges_averaged(self, feedback=True):
        """
        Generates graphs per each condition, where it takes the average of success rate of a
        stimuli from the given condition against how many times the stimuli appeared.

        X axis: Number of times stimuli was presented
        y axis: Relative Accuracy over these 72 trials

        Output: One line for Rank 1 (average all stimuli of rank 1), one line for rank 2 (all
        stimuli of rank 2), one line for rank 3 (all stimuli)
        :param feedback: plot the stimuli with feedback or those without
        """
        plt.title(f"Observed accuracy for possible conditions with{'' if feedback else ' no'} feedback averaged")
        conditions = []
        for i, condition in enumerate(constants.CONDITIONS):
            conditions.append(self.da.get_observed_accuracy_mean_per_condition_all_data_ranges(condition, feedback))
        df = pd.concat(conditions, ignore_index=True, axis=0)
        ax = sns.lineplot(data=df, x=constants.APPEARANCES, y=constants.LOW_REWARD,
                          hue=constants.RANK, sizes=(constants.LOW_REWARD, constants.HIGH_REWARD))
        ax = sns.lineplot(data=df, x=constants.APPEARANCES, y=constants.HIGH_REWARD,
                          hue=constants.RANK, sizes=(constants.LOW_REWARD, constants.HIGH_REWARD))
        for k in range(3):
            ax.lines[k].set_linestyle("--")
        ax.legend(constants.RANK_REWARD_LABELS)
        ax.set(xlabel=constants.APPEARANCES, ylabel=constants.OBSERVED_ACCURACY)
        ax.set(ylim=(0, 1))
        ax.set(xlim=(1, None))
        plt.savefig(f"observed_accuracy_over_trials{'' if feedback else '_no_feedback'}_with_ranges_averaged.pdf")
        plt.clf()

    def observed_accuracy_within_time_differences_conditions_2_4(self, feedback=True):
        """
        Model within conditions 6-4 and 6-2 - by observed accuracy (within feedback trials) but as a function of
        how many blocks they were learned apart

        X axis: Time Difference
        Y Axis: With feedback observed accuracy of second session

        :param feedback: with or without feedback
        """
        plt.title(f"Observed accuracy within time differences across all conditions with"
                  f"{'' if feedback else ' no'} feedback")
        df = self.da.get_within_condition_observed_accuracy_over_time_difference_all_conditions(feedback)
        g = sns.lmplot(data=df.loc[(df[constants.CONDITION] == 2) | (df[constants.CONDITION] == 4)],
                       x=constants.TIME_DIFF, y=constants.OBSERVED_ACCURACY, hue=constants.CONDITION,
                       palette=['green', 'orange'], legend='full', truncate=False)
        g.set(ylim=(0, None))
        for t, l in zip(g._legend.texts, [constants.CONDITIONS_DICT[2], constants.CONDITIONS_DICT[4]]):
            t.set_text(l)
        plt.savefig(
            f"observed_accuracy_within_time_difference_for_{'' if feedback else '_no_feedback'}.pdf")

    def observed_accuracy_within_time_differences(self):
        """
        Model within condition- by observed accuracy (within feedback trials) but as a function of
        how many blocks they were learned apart

        X axis: Time Difference
        Y Axis: With feedback observed accuracy of second session

        """
        plt.title("Observed accuracy within time differences across all conditions with"
                  " feedback")
        df = self.da.get_within_condition_observed_accuracy_over_time_difference_all_conditions(True)
        g = sns.lmplot(data=df, x=constants.TIME_DIFF, y=constants.OBSERVED_ACCURACY, hue=constants.CONDITION,
                       palette=['green', 'orange', 'pink', 'blue'], legend='full', truncate=False)
        g.set(ylim=(0, None))
        for t, l in zip(g._legend.texts, constants.CONDITIONS_DICT.values()):
            t.set_text(l)
        plt.savefig(
            f"observed_accuracy_within_time_difference.pdf")

    def average_accuracy_over_sleep_quality(self):
        """
        Plots average of the subjects accuracy in some day according to their sleep qulaity
        """
        df = self.da.get_mean_success_over_sleep_quality()
        df[constants.SLEEP_SCORE] = df[constants.SLEEP_SCORE].astype(int)

        ax = sns.jointplot(data=df, x=constants.SLEEP_SCORE, y=constants.AVERAGE_ACCURACY, kind="reg",
                           scatter=True, ylim=(0, 1))
        ax.fig.suptitle("Average accuracy in a day over sleep quality")
        ax.fig.subplots_adjust(top=0.93)

        plt.savefig("average_accuracy_over_sleep_quality.pdf")
