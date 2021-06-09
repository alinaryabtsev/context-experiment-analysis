import re


class QuestionnaireManager:

    @staticmethod
    def get_sleep_quality_from_sleep_answer(answer):
        """
        Extracts sleep quality from answer.
        :param answer: string which represents an answer for sleep questionnaire
        :return: number as the sleep quality
        """
        m = re.match('.*overall=(\d+)')
        if m:
            return m.group(1)
        else:
            raise ValueError(f"recieved parameter {answer} has no overall value")
