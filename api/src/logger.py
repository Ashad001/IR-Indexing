import os
import time
import json
import logging
from typing import Dict, List

CONSOLE_LOGS = False



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
