import re
import json
from typing import List, Dict, Tuple, Optional, Any, Set
from inverted_index import InvertedIndex
from porter_stemmer import PorterStemmer as Stemmer
from tokenizer import Tokenizer
from utils import get_logger, timing_decorator, CONSOLE_LOGS
from processor import processor
import queue
import os

class ExtendedBooleanModel:
    def __init__(self, pos_idx: Dict[str, Dict[str, List[int]]], all_docs: List[str]) -> None:
        self.pos_idx: Dict[str, Dict[str, List[int]]] = pos_idx
        self.all_docs: List[int] = [int(i.split('.')[0]) for i in all_docs]
        self.stemmer = Stemmer()
        self.tokenizer = Tokenizer()
        self.logger = get_logger("extended_boolean_model", see_time=True, console_log=CONSOLE_LOGS)
        self.error_logger = get_logger("extended_boolean_model_error", see_time=True, console_log=CONSOLE_LOGS)

    @timing_decorator
    def proximity_query(self, query: str) -> List[int]:
        # Use regular expression to extract words and k from the query
        match = re.match(r'((?:\w+\s?)+) /(\d+)', query)
        if not match:
            return []

        words = match.group(1).split()
        k_str = match.group(2)
        k = int(k_str)
        print(words)
        stemmed_terms = [self.stemmer.stem(word) for word in words]

        result = None
        for i, term in enumerate(stemmed_terms):
            if term in self.pos_idx:
                current_positions = {doc: self.pos_idx[term][doc] for doc in self.pos_idx[term]}
                if result is None:
                    result = current_positions
                else:
                    # Check if positions are k tokens apart
                    new_result = {}
                    for doc in result:
                        if doc in current_positions:
                            positions1 = result[doc]
                            positions2 = current_positions[doc]
                            for pos1 in positions1:
                                for pos2 in positions2:
                                    if abs(pos1 - pos2) <= k:
                                        if doc not in new_result:
                                            new_result[doc] = []
                                        new_result[doc].extend(positions1)
                                        break

                    result = new_result

        if result is not None:
            return list(result.keys())
        else:
            return []

if __name__ == "__main__":
    # ... (unchanged)
    all_docs = os.listdir("../data/ResearchPapers")
    with open("test_pos-index.json", 'r') as f:
        pos_idx = json.load(f)
    ebm = ExtendedBooleanModel(pos_idx, all_docs)

    queries = [
        "perspective looked /2",
        "International Forecasting /2",
        "transformers dependencies capture development /5"
    ]

    for query in queries:
        result = ebm.proximity_query(query)
        print(f"Results for query '{query}': {result}")
