import re
import json
from typing import List, Dict
from src.porter_stemmer import PorterStemmer as Stemmer
from src.tokenizer import Tokenizer
from src.utils import get_logger, timing_decorator, log_message, CONSOLE_LOGS
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
    def search(self, query: str) -> List[int]:
        match = re.match(r'((?:\w+\s?)+) /(\d+)', query)
        if not match:
            return []

        words = match.group(1).split()
        k_str = match.group(2)
        k = int(k_str)
        stemmed_terms = [self.stemmer.stem(word) for word in words]
        print(stemmed_terms)
        result = None
        for i, term in enumerate(stemmed_terms):
            if term in self.pos_idx:
                current_positions = {doc: self.pos_idx[term][doc] for doc in self.pos_idx[term]}
                if result is None:
                    result = current_positions
                else:
                    # Check if all positions are k tokens apart for all words in the query
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
                                        new_result[doc].extend([pos1, pos2])
                                        break

                    result = new_result

        if result is not None:
            # Ensure that the positions are in ascending order
            result = {doc: sorted(positions) for doc, positions in result.items()}
            result = [doc.split('_')[1] for doc in list(result.keys())]
            log_message(json.dumps({"query": query, "documents": result}, indent=4), self.logger, console_log=CONSOLE_LOGS)
            return list(result.keys())

        else:
            return []

if __name__ == "__main__":
    # ... (unchanged)
    all_docs = os.listdir("../data/ResearchPapers")
    with open("../docs/pos-index.json", 'r') as f:
        pos_idx = json.load(f)
    ebm = ExtendedBooleanModel(pos_idx, all_docs)

    queries = [
        "perspective looked /2",
        "International Forecasting /10",
        "Intelligence Concepts Artificial Natural Processing /50",
        "electrocardiographic electronic /4"
    ]

    for query in queries:
        result = ebm.search(query)
        print(f"Results for query '{query}': {result}")
