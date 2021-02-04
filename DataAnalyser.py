import constants
import pandas as pd


class DataAnalyser:
    def __init__(self, db):
        self.db = db
        self.trials = self.db.get_all_trials_with_stimuli()
        self.stimuli = self.db.get_all_stimuli()

    def filter_trials_by_condition_and_probability(self, condition, probability, feedback):
        filtered_stimuli = self.stimuli.loc[(self.stimuli[constants.CONDITION] == condition) &
                                            (self.stimuli[constants.REWARD] == probability)]
        return self.trials.loc[
            ((self.trials[constants.STIM1].isin(filtered_stimuli[constants.NUMBER]) &
              (self.trials[constants.OUTCOME] == constants.FIRST)) |
             (self.trials[constants.STIM2].isin(filtered_stimuli[constants.NUMBER]) &
              (self.trials[constants.OUTCOME] == constants.SECOND))) &
            (self.trials[constants.FEEDBACK] == feedback)]

    def filter_trials_by_condition_and_rank(self, condition, rank, feedback):
        filtered_stimuli = self.stimuli.loc[(self.stimuli[constants.CONDITION] == condition) &
                                            (self.stimuli[constants.RANK] == rank)]
        return self.trials.loc[
            ((self.trials[constants.STIM1].isin(filtered_stimuli[constants.NUMBER]) &
              (self.trials[constants.OUTCOME] == constants.FIRST)) |
             (self.trials[constants.STIM2].isin(filtered_stimuli[constants.NUMBER]) &
              (self.trials[constants.OUTCOME] == constants.SECOND))) &
            (self.trials[constants.FEEDBACK] == feedback)]

    def get_trials_accuracy_by_condition_and_probability(self, condition, probability, feedback):
        filtered = self.filter_trials_by_condition_and_probability(condition, probability, feedback)
        blocks = list(set(filtered[constants.BLOCK].values))
        success_rate = []
        for block in blocks:
            s = len(filtered[(filtered[constants.CHOICE] == filtered[constants.OUTCOME]) &
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
            s = len(filtered[(filtered[constants.CHOICE] == filtered[constants.OUTCOME]) &
                             (filtered[constants.BLOCK] == block)])
            a = len(filtered[filtered[constants.BLOCK] == block])
            success_rate.append(s / a)
        d = {"blocks": blocks, "success rate": success_rate}
        return pd.DataFrame(data=d)

    def get_rt_of_correct_or_incorrect_trials(self, correct, condition=None):
        if condition:
            filtered_stimuli = self.stimuli.loc[self.stimuli[constants.CONDITION] == condition]
            trials_filtered = self.trials.loc[(self.trials[constants.STIM1].isin(
                filtered_stimuli[constants.NUMBER]))]
        else:
            trials_filtered = self.trials
        reaction_times, blocks = [], []
        if correct:
            trials = trials_filtered.loc[trials_filtered[constants.CHOICE] ==
                                         trials_filtered[constants.OUTCOME]]
        else:
            trials = trials_filtered.loc[trials_filtered[constants.CHOICE] !=
                                         trials_filtered[constants.OUTCOME]]
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
