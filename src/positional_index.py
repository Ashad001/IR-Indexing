import re
from typing import List, Optional, Dict, Tuple

class PositionalIndex:
    def __init__(self) -> None:
        self.index: Dict[str, Dict[str, List[int]]] = {}
    
    def add_to_index(self, doc_id: str, tokens: List[str]) -> None:
        """
        adds tokens to index
        
        Args:
            doc_id (str): file id
            tokens (List[str]): list of tokens
        """
        # Extract Doc Id as digit from file name
        file_name = re.findall(r'\d+', doc_id)[0]
        for position, token in enumerate(tokens):
            if token not in self.index:
                self.index[token] = {}
            if doc_id not in self.index[token]:
                self.index[token][doc_id] = []
            self.index[token][doc_id].append(position)
            