import constants
import pandas as pd


class DataAnalyser:
    def __init__(self, db):
        self.db = db
        self.trials = self.db.get_all_trials_with_stimuli()
        self.stimuli = self.db.get_all_stimuli()
        self.stimuli_by_condition = {cond: self.stimuli.loc[(self.stimuli[constants.CONDITION] ==
                                                             cond)] for cond in range(1, 5)}

    def filter_trials_by_condition_and_probability(self, condition, probability, feedback):
        filtered_stimuli = self.stimuli_by_condition[condition]
        filtered_trials = self.trials.loc[(self.trials[constants.FEEDBACK] == feedback)]
        s = filtered_stimuli.set_index(constants.NUMBER)[constants.REWARD]
        m = filtered_trials[
            (filtered_trials[constants.STIM1].map(s).eq(probability) &
             (filtered_trials[constants.STIM1].map(s) > filtered_trials[constants.STIM2].map(s))) |
            (filtered_trials[constants.STIM2].map(s).eq(probability) &
             (filtered_trials[constants.STIM2].map(s) > filtered_trials[constants.STIM1].map(s)))]
        return m

    def filter_trials_by_condition_and_rank(self, condition, rank, feedback):
        filtered_stimuli = self.stimuli.loc[(self.stimuli[constants.CONDITION] == condition)]
        filtered_trials = self.trials.loc[(self.trials[constants.FEEDBACK] == feedback)]
        s = filtered_stimuli.set_index(constants.NUMBER)[constants.RANK]
        m = filtered_trials[
            (filtered_trials[constants.STIM1].map(s).eq(rank) &
             (filtered_trials[constants.STIM1].map(s) > filtered_trials[constants.STIM2].map(s))) |
            (filtered_trials[constants.STIM2].map(s).eq(rank) &
             (filtered_trials[constants.STIM2].map(s) > filtered_trials[constants.STIM1].map(s)))]
        return m

    def get_trials_accuracy_by_condition_and_probability(self, condition, probability, feedback):
        filtered = self.filter_trials_by_condition_and_probability(condition, probability, feedback)
        blocks = list(set(filtered[constants.BLOCK].values))
        success_rate = []
        for block in blocks:
            s = len(filtered[(filtered[constants.OUTCOME] == constants.SUCCESS) &
                             (filtered[constants.BLOCK] == block)])
            a = len(filtered[filtered[constants.BLOCK] == block])
            success_rate.append(s / a)
        d = {"blocks": blocks, "success rate": success_rate}
        return pd.DataFrame(data=d)

    def get_trials_accuracy_by_condition_and_rank(self, condition, rank, feedback):
        filtered = self.filter_trials_by_condition_and_rank(condition, rank, feedback)
        blocks = list(set(filtered[constants.BLOCK].values))
        success_rate = []
        for block in blocks:
            s = len(filtered[(filtered[constants.OUTCOME] == constants.SUCCESS) &
                             (filtered[constants.BLOCK] == block)])
            a = len(filtered[filtered[constants.BLOCK] == block])
            success_rate.append(s / a)
        d = {"blocks": blocks, "success rate": success_rate}
        return pd.DataFrame(data=d)

    def get_rt_of_correct_or_incorrect_trials(self, correct, condition=None,
                                              feedback=constants.WITH_FEEDBACK):
        if condition:
            filtered_stimuli = self.stimuli.loc[self.stimuli[constants.CONDITION] == condition]
            trials_filtered = self.trials.loc[(self.trials[constants.STIM1].isin(
                filtered_stimuli[constants.NUMBER])) & (self.trials[
                                                            constants.FEEDBACK] == feedback)]
        else:
            trials_filtered = self.trials.loc[self.trials[constants.FEEDBACK] == feedback]
        reaction_times, blocks = [], []
        if correct:
            trials = trials_filtered.loc[trials_filtered[constants.OUTCOME] == constants.SUCCESS]
        else:
            trials = trials_filtered.loc[trials_filtered[constants.OUTCOME] == constants.FAILURE]
        for i, trial in trials.iterrows():
            blocks.append(trial[constants.BLOCK])
            reaction_times.append(trial[constants.CHOICE_TIME] - trial[constants.STIM_TIME])
        d = {"blocks": blocks, "rt": reaction_times}
        return pd.DataFrame(data=d)

    @staticmethod
    def _get_rt_means_data_frame(correct, incorrect):
        grouper_correct = correct.groupby("blocks")
        grouper_incorrect = incorrect.groupby("blocks")
        df = grouper_correct["rt"].mean().to_frame(name="RT mean").reset_index()
        df["answer correctness"] = True
        df1 = grouper_incorrect["rt"].mean().to_frame(name="RT mean").reset_index()
        df1["answer correctness"] = False
        return pd.concat([df, df1])

    def get_reaction_time_mean_all_experiment(self):
        correct = self.get_rt_of_correct_or_incorrect_trials(True)
        incorrect = self.get_rt_of_correct_or_incorrect_trials(False)
        return DataAnalyser._get_rt_means_data_frame(correct, incorrect)

    def get_reaction_time_mean_by_condition(self, condition):
        correct = self.get_rt_of_correct_or_incorrect_trials(True, condition)
        incorrect = self.get_rt_of_correct_or_incorrect_trials(False, condition)
        return DataAnalyser._get_rt_means_data_frame(correct, incorrect)

    def _get_all_appearances_of_a_stimuli(self, stim, feedback=True):
        """
        Filters trials table according to given stimuli.
        :param stim: stimuli number
        :param feedback: if True than only stimuli with feedback.
        :return: a table where trials are only of given stimuli.
        """
        return self.trials.loc[(self.trials[constants.FEEDBACK] == feedback) &
                               ((self.trials[constants.STIM1] == stim) |
                                (self.trials[constants.STIM2] == stim))]

    def _get_stimuli_relative_accuracy(self, stim, feedback=True):
        """
        :param stim: stimuli number
        :param feedback: Stimuli with feedback
        :return: a data frame of relative accuracy of a stimuli

        Relative accuracy: for e.g. stim 4- calculate all previous trials with feedback when stim 4
        was chosen. Calculate % of those trials where outcome was 1.
        Relative Correct(stim 4)= (times stim 4 was chosen and outcome==1)/(number of times stim 4
        was chosen) (only need trials table)
        """
        all_stimuli_appearances = self._get_all_appearances_of_a_stimuli(stim, feedback)
        relative_accuracy = [0] * len(all_stimuli_appearances.index)
        chosen_right, chosen, index = 0, 0, 0
        for _, stimuli in all_stimuli_appearances.iterrows():
            if (stimuli[constants.STIM1] == stim and stimuli[constants.CHOICE] ==
                constants.FIRST) or (stimuli[constants.STIM2] and stimuli[constants.CHOICE] ==
                                     constants.FIRST):
                chosen += 1
                if stimuli[constants.OUTCOME] == constants.SUCCESS:
                    chosen_right += 1

            if chosen:
                relative_accuracy[index] = chosen_right / chosen
            index += 1

        relative_accuracy = relative_accuracy[:constants.STIMULI_APPEARANCES_WITH_FEEDBACK]
        return pd.DataFrame(index=list(range(1, len(relative_accuracy) + 1)),
                            data=relative_accuracy,
                            columns=["relative accuracy"])

    def get_relative_accuracy_mean_per_condition(self, condition, feedback=True):
        """
        :param condition: the condition to get relative accuracy mean of its stimuli as a number
        :param feedback: True - than only with feedback.
        :return: a data frame with mean of all stimuli relative accuracy, their ranks according
        to all presented stimuli.
        """
        df = pd.DataFrame()
        all_df = pd.DataFrame()
        for rank in constants.RANKS:
            stimuli_by_rank = self.stimuli_by_condition[condition].loc[(
                self.stimuli_by_condition[condition][constants.RANK] == rank)]
            for _, stim in stimuli_by_rank.iterrows():
                if df.empty:
                    df = self._get_stimuli_relative_accuracy(stim[constants.NUMBER], feedback)
                else:
                    df1 = self._get_stimuli_relative_accuracy(stim[constants.NUMBER], feedback)
                    df = pd.concat([df, df1], axis=1).mean(axis=1)
            df.name = "relative accuracy"
            to_add = pd.DataFrame(df)
            to_add["appearances"] = range(1, len(to_add) + 1)
            to_add[constants.RANK] = str(rank)
            all_df = pd.concat([all_df, to_add], axis=0)
            df = pd.DataFrame()
        return all_df

