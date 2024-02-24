import re
from typing import List, Dict, Tuple, Optional, Any

class BooleanModel:
    def __init__(self) -> None:
        self.index: Dict[str, Dict[str, List[int]]] = {}
    
    def intersection(self, list1: List[int], list2: List[int]) -> List[int]:
        """
        finds intersection of two lists
        
        Args:
            list1 (List[int]): list 1
            list2 (List[int]): list 2
        """
        return list(set(list1).intersection(set(list2)))