class DataAnalyser:
    def __init__(self, db):
        self.db = db
        self.trials = self.db.get_all_trials_with_stimuli()
        self.stimuli = self.db.get_all_stimuli()

    # DEBUG
    def show_trials(self):
        rows = DataAnalyser.filter_trials_by_feedback_value(self.db.get_all_trials_with_stimuli(),1)
        pows = DataAnalyser.filter_trials_by_condition(rows, self.stimuli, 1)
        for block, lst in pows.items():
            print("Length of block is", len(lst))
            print(block, " ", lst)

    @staticmethod
    def filter_trials_by_condition(trials_data, stimuli_data, condition):
        filtered = dict()
        for block, trials in trials_data.items():
            filtered[block] = []
            for trial in trials:
                if stimuli_data[trial["stim1"]]["condition"] == condition:
                    filtered[block].append(trial)
            if not filtered[block]:
                filtered.pop(block)
        return filtered

    @staticmethod
    def filter_trials_by_feedback_value(trials_data, feedback):
        filtered = dict()
        for block, trials in trials_data.items():
            filtered[block] = []
            for trial in trials:
                if trial["feedback"] == feedback:
                    filtered[block].append(trial)
            if not filtered[block]:
                filtered.pop(block)
        return filtered

    def get_trials_filtered_by_condition_and_feedback(self, feedback, condition):
        rows = DataAnalyser.filter_trials_by_feedback_value(self.trials, feedback)
        return DataAnalyser.filter_trials_by_condition(rows, self.stimuli, condition)

    def get_trials_with_stimuli_filtered_by_condition_and_feedback(self, feedback, condition):
        filtered_trials = self.get_trials_filtered_by_condition_and_feedback(feedback, condition)
        for block, trials in filtered_trials.items():
            filtered_trials[block][STIM1]

    #
    # @staticmethod
    # def filter_by_success(trials_data):
    #     filtered = dict()
    #     for block, trials in trials_data.items():
    #         filtered[block] = []
    #         for trial in trials:
    #             if trial["outcome"] == trial["choice"]:
    #                 filtered[block].append(trial)
    #         if not filtered[block]:
    #             filtered.pop(block)
    #     return filtered
