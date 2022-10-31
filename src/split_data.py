# Gist: Splitting the data into training and test subsets and storing in the data/processed dir.

import pandas as pd
import argparse
from sklearn.model_selection import train_test_split
from read_params import read_params
from logger import Logger

# Creating an object of the class Logger.
logger_obj = Logger(logger_name=__name__, file_name=__file__, streamLogs=True)
lgr = logger_obj.get_logger()


def split_and_save(cfile_path):  # cfile_path : Configuration File path.

    try:
        # fetching the relevants
        config = read_params(cfile_path)
        data_path = config["load_data"]["prepared"]
        label = config["base"]["label"]
        test_size = config["split_data"]["test_size"]
        random_state = config["split_data"]["random_state"]

        # paths to save the test and train data
        training_features_path = config["split_data"]["training_features_path"]
        training_labels_path = config["split_data"]["training_labels_path"]
        test_features_path = config["split_data"]["test_features_path"]
        test_labels_path = config["split_data"]["test_labels_path"]

        df = pd.read_csv(data_path)

        # features
        X = df.drop(columns=(label))
        Y = df[label]

        # splitting into training and test subsets
        x_train, x_test, y_train, y_test = train_test_split(
            X, Y, test_size=test_size, random_state=random_state
        )

        # saving them to the data/processed directory
        x_train.to_csv(training_features_path, index=None)
        y_train.to_csv(training_labels_path, index=None)
        x_test.to_csv(test_features_path, index=None)
        y_test.to_csv(test_labels_path, index=None)

    except Exception as e:
        lgr.exception(e)


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parse_args = args.parse_args()
    split_and_save(cfile_path=parse_args.config)
