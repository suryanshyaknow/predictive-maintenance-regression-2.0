# Gist: A function just for reading the params from the `configuration file`.

import yaml
import argparse
import os
from logger import Logger

# Creating an object of the class Logger.
logger_obj = Logger(logger_name=__name__, file_name=__file__, streamLogs=True)
lgr = logger_obj.get_logger()

def read_params(file_path):
    """Read and return the dictionary containing all the paths and params from the parameterized 
    configuration file's path.

    Args:
        file_path (string): Path of the configuration file.

    Returns:
        dict: Contains all the params and paths in the form of key:val pair.
    """
    try:
        with open(file_path) as yaml_file:
            config = yaml.safe_load(yaml_file)
        return config
    except Exception as e:
        lgr.exception(e)

if __name__=="__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parse_args = args.parse_args()
    read_params(file_path=parse_args.config)