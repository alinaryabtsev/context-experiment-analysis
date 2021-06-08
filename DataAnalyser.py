import constants
import pandas as pd
from datetime import datetime
from TimesHelper import TimeHelper


class DataAnalyser:
    def __init__(self, db):
        self.db = db
        self.trials_list = self.db.get_all_trials_with_stimuli()  # list of trials tables from
        # different DBs
        self.stimuli_list = self.db.get_all_stimuli()  # list of stimuli tables from different DBs
        self.trials = self.trials_list[0]
        self.stimuli = self.stimuli_list[0]
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

    def _get_all_appearances_of_a_stimuli(self, stim, feedback=True, db_num=0):
        """
        Filters trials table according to given stimuli.
        :param stim: stimuli number
        :param feedback: if True than only stimuli with feedback.
        :param db_num: number of current db to check
        :return: a table where trials are only of given stimuli.
        """
        trials = self.trials_list[db_num]
        return trials.loc[(trials[constants.FEEDBACK] == feedback) &
                          ((trials[constants.STIM1] == stim) |
                           (trials[constants.STIM2] == stim))]

    def _get_stimuli_relative_accuracy(self, stim, feedback=True, db_num=0):
        """
        :param stim: stimuli number
        :param feedback: Stimuli with feedback
        :param db_num: number of current db to check
        :return: a data frame of relative accuracy of a stimuli

        Relative accuracy: for e.g. stim 4- calculate all previous trials with feedback when stim 4
        was chosen. Calculate % of those trials where outcome was 1.
        Relative Correct(stim 4)= (times stim 4 was chosen and outcome==1)/(number of times stim 4
        was chosen) (only need trials table)
        """
        all_stimuli_appearances = self._get_all_appearances_of_a_stimuli(stim, feedback, db_num)
        relative_accuracy = [0] * len(all_stimuli_appearances.index)
        chosen_right, chosen, index = 0, 0, 0
        for _, stimuli in all_stimuli_appearances.iterrows():
            chosen += 1
            if stimuli[constants.OUTCOME] == constants.SUCCESS:
                chosen_right += 1
            relative_accuracy[index] = chosen_right / chosen
            index += 1
        relative_accuracy = relative_accuracy[:constants.STIMULI_APPEARANCES_WITH_FEEDBACK]
        return pd.DataFrame(index=list(range(1, len(relative_accuracy) + 1)),
                            data=relative_accuracy,
                            columns=[constants.RELATIVE_ACCURACY])

    def _get_stimuli_observed_accuracy(self, stim, feedback=True, db_num=0):
        """
            :param stim: stimuli number
            :param feedback: Stimuli with feedback
            :param db_num: number of current db to check
            :return: a data frame of relative accuracy of a stimuli

            Observed accuracy: unlike relative accuracy, it's also considered when the stimuli is
            not chosen and it shouldn't has been (meaning if outcome = 0 and other stim fixed
            probability is higher)
        """
        all_stimuli_appearances = self._get_all_appearances_of_a_stimuli(stim, feedback, db_num)
        observed_accuracy = [0] * len(all_stimuli_appearances.index)
        chosen_right, chosen, index = 0, 0, 0
        for _, stimuli in all_stimuli_appearances.iterrows():
            chosen += 1
            first, second, outcome, choice = stimuli[constants.FIRST], stimuli[constants.SECOND], \
                                             stimuli[constants.OUTCOME], stimuli[constants.CHOICE]
            first_better = self.has_stimuli_higher_probability(first, second, db_num)
            if outcome == constants.SUCCESS or (outcome == constants.FAILURE and
                                                (choice == constants.FIRST and not first_better)
                                                or (choice == constants.SECOND and first_better)):
                chosen_right += 1
            observed_accuracy[index] = chosen_right / chosen
            index += 1
        observed_accuracy = observed_accuracy[:constants.STIMULI_APPEARANCES_WITH_FEEDBACK]
        return pd.DataFrame(index=list(range(1, len(observed_accuracy) + 1)),
                            data=observed_accuracy,
                            columns=[constants.OBSERVED_ACCURACY])

    def has_stimuli_higher_probability(self, stim1, stim2, db_num):
        """
        Gets two stimuli numbers and than compares which one has a higher probability
        :param stim1: stimulus 1 number
        :param stim2: stimulus 2 number
        :param db_num: the number of the DB
        :return: True if stimulus 1 has higher probability else false
        """
        stimuli = self.stimuli_list[db_num]
        reward1 = stimuli.loc[stimuli[constants.NUMBER] == stim1][constants.REWARD].values[0]
        reward2 = stimuli.loc[stimuli[constants.NUMBER] == stim2][constants.REWARD].values[0]
        return reward1 > reward2

    def get_relative_accuracy_mean_per_condition_all_data(self, condition, feedback=True):
        """
        :param condition: the condition to get relative accuracy mean of its stimuli as a number
        :param feedback: feedback: True - then only with feedback.
        :return: a data frame with mean of all given databases of all stimuli relative accuracy,
        their ranks according to all presented stimuli.
        """
        df = pd.DataFrame(dtype=float)
        df[constants.HIGH_REWARD] = 0
        df[constants.LOW_REWARD] = 0
        rank_to_add = pd.DataFrame(dtype=float)
        all_ranks = pd.DataFrame(dtype=float)
        for rank in constants.RANKS:
            for db_num, stimuli in enumerate(self.stimuli_list):
                stimuli_by_condition = stimuli.loc[(stimuli[constants.CONDITION] == condition)]
                stimuli_by_rank = stimuli_by_condition.loc[(stimuli_by_condition[constants.RANK] == rank)]
                stim_amount, high_reward_amount = 0, 0
                for _, stim in stimuli_by_rank.iterrows():
                    df1 = self._get_stimuli_relative_accuracy(stim[constants.NUMBER], feedback, db_num)
                    if df1.empty:
                        continue
                    stim_amount += 1
                    high_reward_amount += 1 if round(stim[constants.REWARD], 2) == constants.REWARDS_BY_RANK[rank][
                        constants.HIGH_REWARD] else 0
                    df1[constants.HIGH_REWARD], df1[constants.LOW_REWARD] = 0, 0
                    df1[constants.REWARDS_BY_RANK_[rank][round(stim[constants.REWARD], 2)]] = df1[
                        constants.REWARDS_BY_RANK_[rank][round(stim[constants.REWARD], 2)]].add(df1[constants.RELATIVE_ACCURACY])
                    df1 = df1.astype(float)
                    df = df.add(df1, axis=1, fill_value=0)
                df[constants.RELATIVE_ACCURACY] = df[constants.RELATIVE_ACCURACY].div(stim_amount)
                if stim_amount - high_reward_amount:
                    df[constants.LOW_REWARD] = df[constants.LOW_REWARD].div(stim_amount - high_reward_amount)
                if high_reward_amount:
                    df[constants.HIGH_REWARD] = df[constants.HIGH_REWARD].div(high_reward_amount)
                rank_to_add = rank_to_add.add(df, axis=1, fill_value=0)
                df = pd.DataFrame(dtype=float)
            rank_to_add = rank_to_add.divide(len(self.stimuli_list))
            rank_to_add[constants.APPEARANCES] = range(1, len(rank_to_add) + 1)
            rank_to_add[constants.RANK] = str(rank)
            all_ranks = pd.concat([all_ranks, rank_to_add], axis=0)
            rank_to_add = pd.DataFrame()
        all_ranks[constants.RELATIVE_ACCURACY] = all_ranks[constants.RELATIVE_ACCURACY]
        return all_ranks

    def _add_one_dataframe_to_another(self, df, df1):
        for col in [constants.OBSERVED_ACCURACY, constants.LOW_REWARD, constants.HIGH_REWARD]:
            if not df[col].empty and not df[col].isnull().all():
                if len(df.index) > len(df1.index):
                    df[col] = df[col] + df1[col].reindex_like(df[col]).fillna(df1[col].iloc[-1])
                else:
                    df[col] = df1[col] + df[col].reindex_like(df1[col]).fillna(df[col].iloc[-1])
            else:
                df[col] = df1[col]
        return df

    def get_observed_accuracy_mean_per_condition_all_data_ranges(self, condition, feedback=True):
        """
        :param condition: the condition to get relative accuracy mean of its stimuli as a number
        :param feedback: feedback: True - then only with feedback.
        :return: a data frame with mean of all given databases of all stimuli relative accuracy,
        their ranks according to all presented stimuli.
        """
        df = pd.DataFrame(dtype=float)
        df[constants.OBSERVED_ACCURACY], df[constants.LOW_REWARD], df[constants.HIGH_REWARD] = 0, 0, 0
        rank_to_add = pd.DataFrame(dtype=float)
        rank_to_add[constants.OBSERVED_ACCURACY], rank_to_add[constants.LOW_REWARD], rank_to_add[constants.HIGH_REWARD] = 0, 0, 0
        all_ranks = pd.DataFrame(dtype=float)
        for rank in constants.RANKS:
            for db_num, stimuli in enumerate(self.stimuli_list):
                stimuli_by_condition = stimuli.loc[(stimuli[constants.CONDITION] == condition)]
                stimuli_by_rank = stimuli_by_condition.loc[(stimuli_by_condition[constants.RANK] == rank)]
                stim_amount, high_reward_amount = 0, 0
                for _, stim in stimuli_by_rank.iterrows():
                    df1 = self._get_stimuli_observed_accuracy(stim[constants.NUMBER], feedback, db_num)
                    if df1.empty:
                        continue
                    stim_amount += 1
                    high_reward_amount += 1 if round(stim[constants.REWARD], 2) == constants.REWARDS_BY_RANK[rank][
                        constants.HIGH_REWARD] else 0
                    df1[constants.HIGH_REWARD], df1[constants.LOW_REWARD] = 0, 0
                    df1[constants.REWARDS_BY_RANK_[rank][round(stim[constants.REWARD], 2)]] = df1[
                        constants.REWARDS_BY_RANK_[rank][round(stim[constants.REWARD], 2)]].add(
                        df1[constants.OBSERVED_ACCURACY]).astype(float)
                    df = self._add_one_dataframe_to_another(df, df1)
                df[constants.OBSERVED_ACCURACY] = df[constants.OBSERVED_ACCURACY].div(stim_amount)
                if stim_amount - high_reward_amount:
                    df[constants.LOW_REWARD] = df[constants.LOW_REWARD].div(stim_amount - high_reward_amount)
                if high_reward_amount:
                    df[constants.HIGH_REWARD] = df[constants.HIGH_REWARD].div(high_reward_amount)
                rank_to_add = self._add_one_dataframe_to_another(rank_to_add, df)
                df = pd.DataFrame(dtype=float)
                df[constants.OBSERVED_ACCURACY], df[constants.LOW_REWARD], df[constants.HIGH_REWARD] = 0, 0, 0
            rank_to_add = rank_to_add.divide(len(self.stimuli_list))
            rank_to_add[constants.APPEARANCES] = range(1, len(rank_to_add) + 1)
            rank_to_add[constants.RANK] = str(rank)
            all_ranks = pd.concat([all_ranks, rank_to_add], axis=0)
            rank_to_add = pd.DataFrame()
            rank_to_add[constants.OBSERVED_ACCURACY], rank_to_add[constants.LOW_REWARD], rank_to_add[
                constants.HIGH_REWARD] = 0, 0, 0
        all_ranks[constants.OBSERVED_ACCURACY] = all_ranks[constants.OBSERVED_ACCURACY]
        return all_ranks

    def get_observed_accuracy_mean_per_condition_all_data(self, condition, feedback=True):
        """
        :param condition: the condition to get observed accuracy mean of its stimuli as a number
        :param feedback: feedback: True - then only with feedback.
        :return: a data frame with mean of all given databases of all stimuli relative accuracy,
        their ranks according to all presented stimuli.
        """
        df = pd.DataFrame()
        rank_to_add = pd.DataFrame()
        all_ranks = pd.DataFrame()
        for rank in constants.RANKS:
            for db_num, stimuli in enumerate(self.stimuli_list):
                stimuli_by_condition = stimuli.loc[(stimuli[constants.CONDITION] == condition)]
                stimuli_by_rank = stimuli_by_condition.loc[(stimuli_by_condition[constants.RANK] == rank)]
                number_of_stimuli = 0
                for _, stim in stimuli_by_rank.iterrows():
                    df1 = self._get_stimuli_observed_accuracy(stim[constants.NUMBER], feedback, db_num)
                    number_of_stimuli += 1 if not df1.empty else 0
                    df = df.add(df1, axis=1, fill_value=0)
                df = df.divide(number_of_stimuli)
                rank_to_add = rank_to_add.add(df, axis=1, fill_value=0)
                df = pd.DataFrame()
            rank_to_add = rank_to_add.divide(len(self.stimuli_list))
            rank_to_add[constants.APPEARANCES] = range(1, len(rank_to_add) + 1)
            rank_to_add[constants.RANK] = str(rank)
            all_ranks = pd.concat([all_ranks, rank_to_add], axis=0)
            rank_to_add = pd.DataFrame()
        all_ranks[constants.OBSERVED_ACCURACY] = all_ranks[constants.OBSERVED_ACCURACY].astype(float)
        return all_ranks

    def get_within_condition_relative_accuracy_over_time_difference(self, condition, feedback=True):
        """
        Model within condition- accuracy (within feedback trials) but as a function of how many
        blocks they were learned apart.
        X axis: Time Difference
        Y Axis (Separately):   1) Feedback accuracy of second session
                               2) No Feedback Accuracy (separate for each condition)

        E.g. in a 3-2 condition stimulus 3
            1. Calculate the end time of the first block with stimulus 3
            2. Calculate the start time of the 2nd block with stimulus 3
            __________________________________
            Time difference

            1. Take all no feedback trials where stimulus 3 was presented
            2, Take their mean relative accuracy

        _____________________________
        This produces a single point for the y axis

        Iterate over all stimuli (63 points)

        :param feedback: with or without feedback
        :param condition: condition of the data
        :return: data frame for
        """
        df = pd.DataFrame()
        all_data = pd.DataFrame()
        for db_num, stimuli in enumerate(self.stimuli_list):
            stimuli_by_condition = stimuli.loc[(stimuli[constants.CONDITION] == condition)]
            for _, stim in stimuli_by_condition.iterrows():
                relative_accuracy = \
                    self._get_stimuli_relative_accuracy(stim[constants.NUMBER], feedback, db_num)[
                        constants.RELATIVE_ACCURACY].mean()
                stimuli_trials = self._get_all_appearances_of_a_stimuli(stim[constants.NUMBER],
                                                                        feedback, db_num)
                if stimuli_trials.empty:
                    continue
                stimuli_blocks = stimuli_trials[constants.BLOCK].unique()
                if condition in constants.CONDITIONS[:2]:
                    time_diff = TimeHelper.calculate_time_differences_between_blocks(
                        stimuli_trials, *stimuli_blocks)
                else:
                    time_diff = TimeHelper.calculate_time_differences_between_blocks(
                        stimuli_trials, *stimuli_blocks[1:3])
                df = df.append(pd.DataFrame({constants.RELATIVE_ACCURACY: [relative_accuracy],
                                             constants.TIME_DIFF: [time_diff],
                                             constants.NUMBER: [stim[constants.NUMBER]]}),
                               ignore_index=True)
            all_data = all_data.add(df, axis=1, fill_value=0)
            df = pd.DataFrame()
        all_data = all_data.divide(len(self.stimuli_list))
        all_data[constants.CONDITION] = condition
        return all_data

    def get_within_condition_observed_accuracy_over_time_difference(self, condition, feedback=True):
        """
        Model within condition- observed accuracy (within feedback trials) but as a function of how
        many blocks they were learned apart.
        X axis: Time Difference
        Y Axis (Separately):   1) Feedback observed accuracy of second session
                               2) No Feedback observed Accuracy (separate for each condition)

        E.g. in a 3-2 condition stimulus 3
            1. Calculate the end time of the first block with stimulus 3
            2. Calculate the start time of the 2nd block with stimulus 3
            __________________________________
            Time difference

            1. Take all no feedback trials where stimulus 3 was presented
            2, Take their mean observed accuracy

        _____________________________
        This produces a single point for the y axis

        Iterate over all stimuli (63 points)

        :param feedback: with or without feedback
        :param condition: condition of the data
        :return: data frame with observed accuracies and time differences they have been learned
        """
        df = pd.DataFrame()
        all_data = pd.DataFrame()
        for db_num, stimuli in enumerate(self.stimuli_list):
            stimuli_by_condition = stimuli.loc[(stimuli[constants.CONDITION] == condition)]
            for _, stim in stimuli_by_condition.iterrows():
                observed_accuracy = \
                    self._get_stimuli_observed_accuracy(stim[constants.NUMBER], feedback, db_num)[
                        constants.OBSERVED_ACCURACY].mean()
                stimuli_trials = self._get_all_appearances_of_a_stimuli(stim[constants.NUMBER], db_num=db_num)
                if stimuli_trials.empty:
                    continue
                stimuli_blocks = stimuli_trials[constants.BLOCK].unique()
                if condition in constants.CONDITIONS[:2]:
                    time_diff = TimeHelper.calculate_time_differences_between_blocks(stimuli_trials, *stimuli_blocks)
                else:
                    time_diff = TimeHelper.calculate_time_differences_between_blocks(stimuli_trials, *stimuli_blocks[1:3])
                df = df.append(pd.DataFrame({constants.OBSERVED_ACCURACY: [observed_accuracy],
                                             constants.TIME_DIFF: [time_diff],
                                             constants.NUMBER: [stim[constants.NUMBER]]}),
                               ignore_index=True)
            all_data = all_data.add(df, axis=1, fill_value=0)
            df = pd.DataFrame()
        all_data = all_data.divide(len(self.stimuli_list))
        all_data[constants.CONDITION] = condition
        return all_data

    def get_within_condition_accuracy_over_time_difference_all_conditions(self, feedback=True):
        """
        gets data over all conditions of Model within condition- accuracy (within feedback trials)
        but as a function of how many blocks they were learned apart

        :param feedback: data with feedback or without
        :return: data frame with all the of the
        """
        df = pd.DataFrame()
        for condition in constants.CONDITIONS:
            df = df.append(self.get_within_condition_relative_accuracy_over_time_difference(condition, feedback))
        return df

    def get_within_condition_observed_accuracy_over_time_difference_all_conditions(self, feedback=True):
        """
        gets data over all conditions of Model within condition- accuracy (within feedback trials)
        but as a function of how many blocks they were learned apart

        :param feedback: data with feedback or without
        :return: data frame with all the of the oredered trials data
        """
        df = pd.DataFrame()
        for condition in constants.CONDITIONS:
            df = df.append(self.get_within_condition_observed_accuracy_over_time_difference(condition,
                                                                                   feedback))
        return df
