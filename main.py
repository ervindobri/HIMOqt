import myo
from helpers import classification as clf
from helpers.constants import *


def main():
    myo.init(sdk_path=os.getcwd())
    # name = input("Enter subject name")
    x = clf.Classification(
        # subject=name,
        subject_name="Ervin",
        subject_age=22,
        batch_size=25,
    )
    # x.PrepareTrainingData()
    # history = x.TrainEMG()
    # x.DisplayResult(history)

    x.TestLatency(50)


if __name__ == '__main__':
    main()
