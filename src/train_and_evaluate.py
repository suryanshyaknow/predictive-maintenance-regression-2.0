# Gist: Standardization of features, training an algorithm, building the model and saving it and evaluation.

import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from read_params import read_params
from logger import Logger

import pickle
import json
import os
import argparse

# Creating an object of the class Logger.
logger_obj = Logger(logger_name=__name__, file_name=__file__, streamLogs=True)
lgr = logger_obj.get_logger()


class Model:
    """A class for scaling the features, then build the linear regression model out of it and training labels,
    model's evaluation using `r-squared` or `adjusted r-squared` metrics and eventually save the model.
    """

    def __init__(self, cfile_path):
        """__init__ method for the class Model.

        Args:
            cfile_path (string): Configuration file path.
        """
        try:
            # for fetching DEPENDENCIES we gotta read the params from the config file
            config = read_params(cfile_path)

            # TRAINING data
            x_train_path = config["split_data"]["training_features_path"]
            self.x_train = pd.read_csv(x_train_path)  # loading the training features
            y_train_path = config["split_data"]["training_labels_path"]
            self.y_train = pd.read_csv(y_train_path)  # loading the training labels

            # TEST data
            x_test_path = config["split_data"]["test_features_path"]
            self.x_test = pd.read_csv(x_test_path)  # loading the test features
            y_test_path = config["split_data"]["test_labels_path"]
            self.y_test = pd.read_csv(y_test_path)

            # STANDARDIZATION of FEATURES
            self.scaler = StandardScaler()
            self.x_scaled = self._standardize()
            # Saving the StandardScaler object
            self.scaler_dir = config["transformation_dir"]["dir"]
            self._save_scaler()

            # building the MODEL..
            self.mod = self._build()  # model
            lgr.info("Model built successsfully!")

            # EVALUATION using `r-squared` and `ajusted r-squared` SCORES.
            self.scores_dir = config["reports"]["dir"]
            self._evaluate_and_report()

            # Dir to SAVE the MODEL into..
            self.mod_dir = config["model_dir"]["dir"]
            # Saving the MODEL to the 'saved_models' dir.
            self._save()

        except Exception as e:
            lgr.exception(e)

    def _standardize(self):
        """Standardizes the training features via StandardScaler.

        Returns:
            np.array: Scaled features with their Mean = 0 and Standard Deviation = 1.
        """
        try:
            lgr.info("Scaling the features to the normal scale..")
            self.scaler.fit(self.x_train)
            lgr.info("..standardization done!")
            return self.scaler.transform(self.x_train)

        except Exception as e:
            lgr.exception(e)

    def _save_scaler(self):
        """Saves the scaler object in the transformation dir.
        """
        try:
            lgr.info("saving the scaler object..")
            os.makedirs(self.scaler_dir, exist_ok=True)
            with open(os.path.join(self.scaler_dir, 'scaler.pkl'), 'wb') as f:
                pickle.dump(self.scaler, file=f)
            lgr.info(f'scaler object saved successfully at "{self.scaler_dir}"')

        except Exception as e:
            lgr.exception(e)

    def _build(self):
        try:
            lgr.info(
                "fitting the training data and building the Linear Regression model..")
            mod = LinearRegression()
            mod.fit(self.x_scaled, self.y_train)
            return mod

        except Exception as e:
            lgr.exception(e)

    def _save(self):
        try:
            os.makedirs(self.mod_dir, exist_ok=True)
            lgr.info("saving the model..")
            with open(os.path.join(self.mod_dir, 'model.pkl'), 'wb') as f:
                pickle.dump(self.mod, file=f)
            lgr.info(f"The model is successfully saved at '{self.mod_dir}'")

        except Exception as e:
            lgr.exception(e)

    def _evaluate_and_report(self):
        """Evaluate the model accuracy on test set as well as on training via `R-squared` and `Adjusted R-squared`
        scores and creating the score report.
        """
        try:
            lgr.info("Evaluating the metrics..")

            # Scaling the test features too!
            x_test_scaled = self.scaler.transform(
                self.x_test)

            # R-squared score
            # TEST SCORE
            test_r2 = round(self.mod.score(x_test_scaled, self.y_test), 3)
            lgr.info(
                f"The `R-squared score` of the model on the test set is {test_r2}.")
            # TRAINING SCORE
            training_r2 = round(self.mod.score(self.x_scaled, self.y_train), 3)
            lgr.info(
                f"The `R-squared score` of the model on the training set is {training_r2}.")

            # Adjusted R-squared
            """
            Adjusted R-squared  = 1 - ((n-1)*(1 - R-squared) / (n-p-1))
                where n = Total Sample size
                      p = Number of Independent Predictors
            """
            n = self.x_train.shape[0]
            p = len(self.x_train.columns)

            # TEST Adjusted R-squared Score
            test_adjusted_r2 = round(1 - ((n-1)*(1 - test_r2) / (n-p-1)), 3)
            lgr.info(
                f"The `Adjusted R-squared score` of the model on the test set is {test_adjusted_r2}.")

            # TRAINING Adjusted R-squared Score
            training_adjusted_r2 = round(1 - ((n-1)*(1 - training_r2) / (n-p-1)), 3)
            lgr.info(
                f"The `Adjusted R-squared score` of the model on the test set is {training_adjusted_r2}.")

            # SAVING the SCORES to the REPORTS dir
            os.makedirs(self.scores_dir, exist_ok=True)
            with open(os.path.join(self.scores_dir, 'scores.json'), 'w') as f:
                scores = {
                    "Training Accuracies": {"R-squared": training_r2,
                                            "Adjusted R-squared": training_adjusted_r2},
                    "Test Accuracies": {"R-squared": training_r2,
                                        "Adjusted R-squared": test_adjusted_r2}
                }
                json.dump(scores, f, indent=4)

        except Exception as e:
            lgr.exception(e)


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parse_args = args.parse_args()
    Model(cfile_path=parse_args.config)
