from datetime import datetime
import constants


class TimeHelper:

    @staticmethod
    def calculate_time_differences_between_blocks(stimuli, start_block, end_block):
        """
        Gets two blocks' numbers of some stimuli and calculates time difference between last
        appearance of the first block and time difference of the first appearance of the second
        block.
        :param stimuli: stimuli appearances dataframe
        :param start_block: block number of the first block to calculate time difference
        :param end_block: block number of the seconds block to calculate time difference
        :return: time difference in hours between two appearances of the blocks
        """
        t1 = datetime.fromtimestamp(stimuli.loc[stimuli[constants.BLOCK] == start_block].tail(
            1).iloc[0][constants.CHOICE_TIME] / 1000)
        t2 = datetime.fromtimestamp(stimuli.loc[stimuli[constants.BLOCK] == end_block].head(
            1).iloc[0][constants.CHOICE_TIME] / 1000)
        return abs(t1 - t2).total_seconds() / 3600

    @staticmethod
    def calculate_time_differences_between_appearances(first_appearance, second_appearance):
        """
        Gets two stimuli appearances and calculates time difference of the first appearance and the second appearance.
        :param first_appearance: first appearance of a stimuli in a trial Series
        :param second_appearance: first appearance of a stimuli in a trial Series
        :return: time difference in hours between two appearances of the stimuli
        """
        t1 = datetime.fromtimestamp(first_appearance.iloc[0][constants.CHOICE_TIME] / 1000)
        t2 = datetime.fromtimestamp(second_appearance.iloc[0][constants.CHOICE_TIME] / 1000)
        return abs(t1 - t2).total_seconds() / 3600
