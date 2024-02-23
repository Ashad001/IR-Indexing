import re
import json
import heapq
from typing import Any, Tuple, Dict, List, Optional

class InvertedIndex:
    def __init__(self, load_from_file=False) -> None:
        self.index: Dict[str, Dict[str, List[int]]] = {}
        if load_from_file:
            self.load_index()
    
    def load_index(self) -> None:
        """
        Loads index from file
        """
        with open("test_inv-index.json", 'r', encoding='utf-8') as f:
            self.index = json.load(f)
    
    def add_to_index(self, doc_id: str, tokens: List[str]) -> None:
        """
        adds tokens to index
        
        Args:
            doc_id (str): file id
            tokens (List[str]): list of tokens
        """
        for token in tokens:
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