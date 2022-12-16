import yaml

from pathlib import Path

def get_path():
    """
    A function to get the current path to main.py
    Returns:
     - cwd (string) : Path to main.py directory
    """
    cwd = Path(__file__).parents[1]
    cwd = str(cwd)
    return cwd



def read_yml(filename):
    """
    A function to read a yml file and return the data.
    Params:
     - filename (string) : The name of the file to open
    Returns:
     - data (dict) : A dict of the data in the file
    """
    cwd = get_path()
    # if filename.startswith("config"):
    cd = cwd.replace('util', '')
    with open(cd + filename + ".yml", "r") as file:
        data = yaml.safe_load(file)
    return data