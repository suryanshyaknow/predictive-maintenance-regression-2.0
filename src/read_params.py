# Gist: A function just for reading the params from the `configuration file`.

import yaml
import argparse

def read_params(file_path):
    """Read and return the dictionary containing all the paths and params from the parameterized 
    configuration file's path.

    Args:
        file_path (string): Path of the configuration file.

    Returns:
        dict: Contains all the params and paths in the form of key:val pair.
    """
    with open(file_path) as yaml_file:
        config = yaml.safe_load(yaml_file)

    return config

if __name__=="__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parse_args = args.parse_args()
    read_params(file_path=parse_args.config)