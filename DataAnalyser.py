class DataAnalyser:
    def __init__(self, db):
        self.db = db

    def show_stimuli(self):
        for row in self.db.get_all_stimuli().items():
            print(row)

    def get_stimuli(self):
        return self.db.get_all_stimuli()

    def get_trials(self):
        return self.db.get_all_trials_with_stimuli()

    # DEBUG
    def show_trials(self):
        rows = DataAnalyser.filter_trials_by_feedback_value(self.db.get_all_trials_with_stimuli(),1)
        pows = DataAnalyser.filter_trials_by_condition(rows, self.get_stimuli(), 1)
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
        rows = DataAnalyser.filter_trials_by_feedback_value(self.db.get_all_trials_with_stimuli(),
                                                            feedback)
        return DataAnalyser.filter_trials_by_condition(rows, self.get_stimuli(), condition)

    @staticmethod
    def filter_by_success(trials_data):
        filtered = dict()
        for block, trials in trials_data.items():
            filtered[block] = []
            for trial in trials:
                if trial["outcome"] == trial["choice"]:
                    filtered[block].append(trial)
            if not filtered[block]:
                filtered.pop(block)
        return filtered
