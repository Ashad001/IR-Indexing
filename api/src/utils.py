import os
import time
import json
from src.logger import get_logger, log_message
from typing import Dict, List

CONSOLE_LOGS = False

def list_files(directory: str, exclude_files: List[str]) -> List[str]:
    """
    List all files in a directory

    Args:
        directory (str): directory path to list files from i.e. ./data
        exclude_files (List[str]): exclude files from the list such as stopwords

    Returns:
        List[str]: files list in the directory
    """
    file_list = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if file not in exclude_files and os.path.isfile(file_path):
                file_list.append(file_path)

    return file_list

def read_data(file_name: str) -> str:
    """
    reads data from file

    Args:
        file_name (str): file name
    """
    with open(file_name, "r", encoding='utf-8', errors='ignore') as file:
        data = file.read()
    return data

def write_data(file_name: str, data: Dict[str, Dict[str, List[int]]]) -> None:
    """
    writes data to file

    Args:
        file_name (str): file name
        data (List[str]): data to write
    """
    with open(file_name, "w", encoding="utf-8", errors='ignore') as file:
        json.dump(data, file, indent=4)


def read_metadata(name: str) -> List[Dict[str, str]]:
    data = ""
    if os.path.exists(f"./logs/{name}.log"):
        with open(f"./logs/{name}.log", "r") as f:
            data = f.read()
        data = "[" + data[: (len(data) - 2)] + "]"
        data = json.loads(data)
    return data


def timing_decorator(func):
    """
    Decorator that logs the execution time of a function.

    Args:
        func: The function to be decorated.

    Returns:
        The decorated function.
    """

    def wrapper(*args, **kwargs):
        logger = get_logger(
            func.__name__ + "_time_log", see_time=True, console_log=CONSOLE_LOGS
        )
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        log_message(
            f"Function {func.__name__} from {func.__qualname__} took {elapsed_time:.4f} seconds to run.", logger
        )
        return result

    return wrapper
