import re
import json
from typing import List, Optional, Dict, Tuple

class PositionalIndex:
    def __init__(self, load_from_file: bool = False) -> None:
        self.index: Dict[str, Dict[str, List[int]]] = {}
        if load_from_file:
            self.load_index()
        
    def load_index(self) -> None:
        """
        Loads index from file
        """
        with open("test_pos-index.json", 'r', encoding='utf-8') as f:
            self.index = json.load(f)
    
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
            