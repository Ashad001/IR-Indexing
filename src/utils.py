import os
import re
import time
import json
import logging
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

def read_data(file_name: str) -> List[str]:
    """
    reads data from file

    Args:
        file_name (str): file name
    """
    with open(file_name, "r") as file:
        data = file.read()
    return data


def write_data(file_name: str, data: Dict[str, Dict[str, List[int]]]) -> None:
    """
    writes data to file

    Args:
        file_name (str): file name
        data (List[str]): data to write
    """
    with open(file_name, "w") as file:
        json.dump(data, file, indent=4)


def read_metadata(name: str) -> List[Dict[str, str]]:
    data = ""
    if os.path.exists(f"./logs/{name}.log"):
        with open(f"./logs/{name}.log", "r") as f:
            data = f.read()
        data = "[" + data[: (len(data) - 2)] + "]"
        data = json.loads(data)
    return data


def get_logger(
    name: str,
    see_time: bool = False,
    console_log: bool = False,
    level: int = logging.INFO,
) -> logging.Logger:
    """
    Returns a logger object

    Args:
        name (str): Name of the logger
        level (int): Logging level
    """
    os.makedirs("./logs", exist_ok=True)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    if see_time:
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
    else:
        formatter = logging.Formatter("%(message)s,")

    file_handler = logging.FileHandler(f"./logs/{name}.log")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    if console_log:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger


def log_message(
    message: str, logger: logging.Logger, level: int = logging.INFO
) -> None:
    """
    Logs a message

    Args:
        message (str): Message to be logged
        logger (logging.Logger): Logger object
        level (int): Logging level
    """
    if level == logging.INFO:
        logger.info(message)
    elif level == logging.ERROR:
        logger.error(message)
    elif level == logging.WARNING:
        logger.warning(message)
    elif level == logging.DEBUG:
        logger.debug(message)
    else:
        logger.info(message)


def metadata_lookup(
    meta_data, data: List[Dict[str, str]], logger: logging.Logger
) -> bool:
    """
    Looks up metadata for a document

    Args:
        doc_id (str): Document ID
        logger (logging.Logger): Logger object
    """
    logger.info(f"Looking up metadata for {meta_data['doc_id']}")
    # if os.path.exists(f"./logs/{name}.log"):
    #     with open(f"./logs/{name}.log", "r") as f:
    #         data = f.read()
    # data = "[" + data[: (len(data) - 2)] + "]"
    # data = json.loads(data)
    meta_doc_ids = []
    for x in data:
        if x["doc_id"] == meta_data.get("doc_id"):
            if "inv_index_file" in x and "pos_index_file" in x and "vocab_file" in x:
                meta_doc_ids.append(x["doc_id"])
                
    if meta_data["doc_id"] in meta_doc_ids:
        log_message(
            f"Processing already done for {meta_data['doc_id']}.txt",
            logger,
            logging.INFO,
        )
        return True
    else:
        log_message(
            f"Metadata for {meta_data['doc_id']} not found", logger, logging.WARNING
        )
    return False


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
