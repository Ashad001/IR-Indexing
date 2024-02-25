import re
import json
import logging
from typing import List, Optional, Dict, Tuple
from utils import log_message, get_logger
class PositionalIndex:
    def __init__(self) -> None:
        self.index: Dict[str, Dict[str, List[int]]] = {}
        
    def load_from_index(self, file_name: str, logger: logging.Logger) -> None:
        """
        Load saved index from file

        Args:
            file_name (str): Full path to the file
        """
        try:
            with open(file_name, 'r', encoding='utf-8') as f:
                self.index = json.load(f)
        except FileNotFoundError:
            log_message(f"{file_name} not found for loading positional index", logger, level=logging.ERROR)
            pass
        
    def add_to_index(self, doc_id: str, tokens: List[str]) -> None:
        """
        adds tokens to index
        
        Args:
            doc_id (str): file id
            tokens (List[str]): list of tokens
        """
        # Extract Doc Id as digit from file name
        for position, token in enumerate(tokens):
            if token not in self.index:
                self.index[token] = {}
            if doc_id not in self.index[token]:
                self.index[token][doc_id] = []
            self.index[token][doc_id].append(position)
            