## Gist: Read the params and return the dataframe.

from asyncore import read
import os
import yaml
import pandas as pd
import argparse
from read_params import read_params


def get_data(config_path):
    """A function to fetch the data by reading the parameters from the parameterized path 
    i.e. `Configuration Path` containing all the paths and parameters.

    Args:
        config_path (string): Configuration path for fetching the dataset.
    """
    # reading the parameters to fetch the data path, from the config_path.
    config = read_params(config_path)

    data_path = config["data_source"]["s3_source"]
    print(config)
    return pd.read_csv(data_path)


if __name__=="__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parse_args = args.parse_args()
    get_data(config_path=parse_args.config)