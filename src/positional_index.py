import re
from typing import List, Optional, Dict, Tuple

class PositionalIndex:
    def __init__(self) -> None:
        self.index: Dict[str, Dict[str, List[int]]] = {}
    
    def add_to_index(self, file_name: str, tokens: List[str]) -> None:
        """
        adds tokens to index
        
        Args:
            file_name (str): file name
            tokens (List[str]): list of tokens
        """
        # Extract Doc Id as digit from file name
        file_name = re.findall(r'\d+', file_name)[0]
        for position, token in enumerate(tokens):
            if token not in self.index:
                self.index[token] = {}
            if file_name not in self.index[token]:
                self.index[token][file_name] = []
            self.index[token][file_name].append(position)
            