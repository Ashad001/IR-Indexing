import re
import heapq
from typing import Any, Tuple, Dict, List, Optional

class InvertedIndex:
    def __init__(self) -> None:
        self.index: Dict[str, Dict[str, List[int]]] = {}
    
    def add_to_index(self, file_name: str, tokens: List[str]) -> None:
        """
        adds tokens to index
        
        Args:
            file_name (str): file name
            tokens (List[str]): list of tokens
        """
        for token in tokens:
            if token not in self.index:
                self.index[token] = {}
            if file_name not in self.index[token]:
                self.index[token][file_name] = 0
            self.index[token][file_name] += 1
            
        #! NEEDS FIX: Two Time Data Loopup
        for token in tokens:
            self.sort_token_counts(token)
       
    def sort_token_counts(self, token: str) -> None:
        """
        Sorts the token counts for a given token in descending order.

        Args:
            token (str): Token.
        """
        self.index[token] = dict(heapq.nlargest(len(self.index[token]), self.index[token].items(), key=lambda item: item[1]))