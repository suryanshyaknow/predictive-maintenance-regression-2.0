# Gist: Read the params and return the dataframe.

from logger import Logger
import pandas as pd
import argparse
from read_params import read_params

# Creating an object of the class Logger.
logger_obj = Logger(logger_name=__name__, file_name=__file__, streamLogs=True)
lgr = logger_obj.get_logger()


def get_data(config_path):
    """A function to fetch the data by reading the parameters from the parameterized path
    i.e. `Configuration Path` containing all the paths and parameters.

    Args:
        config_path (string): Configuration path for fetching the dataset.
    """
    try:
        # reading the parameters to fetch the data path, from the config_path.
        config = read_params(config_path)
        data_path = config["data_source"]["s3_source"]
        return pd.read_csv(data_path)
    except Exception as e:
        lgr.exception(e)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="params.yaml")
    parse_args = parser.parse_args()
    get_data(config_path=parse_args.config)
