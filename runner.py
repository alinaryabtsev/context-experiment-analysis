from DataAnalyser import DataAnalyser
import DataBaseManager
from STLearningAcrossConditions import ShortTermLearningAcrossConditions

DATABASE_FILE_NAME = "001_schedule.db"


def main():
    db = DataBaseManager.DataBaseManager(DATABASE_FILE_NAME)
    analyser = ShortTermLearningAcrossConditions(db)
    # analyser.show_trials()


if __name__ == '__main__':
    main()
