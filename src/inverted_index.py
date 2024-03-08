import re
import json
import heapq
import logging
from typing import   Dict, List
from src.utils import log_message
class InvertedIndex:
    def __init__(self, load_from_file=False) -> None:
        self.index: Dict[str, Dict[str, List[int]]] = {}
        if load_from_file:
            self.load_index()
    
    def load_from_file(self, file_name: str, logger: logging.Logger) -> None:
        """
        Load saved index from file

        Args:
            file_name (str): Full path to the file
        """
        try:
            with open(file_name, 'r', encoding='utf-8') as f:
                local_inv_idx = json.load(f)
                for doc_id, local_inv in local_inv_idx.items():
                    self.index.setdefault(doc_id, {}).update(local_inv)
        except FileNotFoundError:
            log_message(f"{file_name} not found for loading positional index", logger, level=logging.ERROR)
            pass
    
    def add_to_index(self, doc_id: str, token: str) -> None:
        """
        adds token to index
        
        Args:
            token (str): token
            doc_id (str): file id
        """
        if token not in self.index:
            self.index[token] = {}
        if doc_id not in self.index[token]:
            self.index[token][doc_id] = 0
        self.index[token][doc_id] += 1
            
        #! NEEDS FIX: Two Time Data Lookup
        # for token in tokens:
            # self.sort_token_counts(token)
       
    def sort_token_counts(self, token: str) -> None:
        """
        Sorts the token counts for a given token in descending order.

        Args:
            token (str): Token.
        """
        self.index[token] = dict(heapq.nlargest(len(self.index[token]), self.index[token].items(), key=lambda item: item[1]))