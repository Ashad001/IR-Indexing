import re
import json
from typing import List, Dict, Tuple, Optional, Any, Set
# Assuming the below imports work as intended
from inverted_index import InvertedIndex
from porter_stemmer import PorterStemmer as Stemmer
from tokenizer import Tokenizer
from utils import get_logger, timing_decorator
from processor import processor
import queue
import os

class BooleanModel:
    def __init__(self) -> None:
        processor('../data/ResearchPapers')
        self.inv_idx = None
        with open(f'test_inv-index.json', 'r') as f:
            self.inv_idx = json.load(f)
        self.all_docs = len(os.listdir('../data/ResearchPapers'))
        self.all_docs = [i for i in range(1, self.all_docs + 1)]
        self.stemmer = Stemmer()
        self.tokenizer = Tokenizer()
        self.logger = get_logger("boolean_model", see_time=True, console_log=True)
        self.error_logger = get_logger("boolean_model_error", see_time=True, console_log=True)
    
    @timing_decorator
    def process_query(self, query: str) -> List[str]:
        tokens = self.tokenizer.tokenize(query)
        words = [self.stemmer.stem(word.lower()) for word in tokens if word.upper() not in ['AND', 'OR', 'NOT']]
        print(words)
        postings = self.get_postings(words)
        if len(postings) == 0:
            return []
        documents = self.evaluate_query(postings, tokens)
        documents = [int(doc) for doc in documents]
        return documents

    
    def evaluate_query(self, postings: List[Dict[str, List[int]]], query_tokens: List[str]) -> List[int]: 
        if len(postings) == 1:
            if query_tokens[0] == 'NOT':
                return self.not_op(list(postings[0].values())[0])
            return list(postings[0].values())[0]
        elif len(postings) == 2:
            if query_tokens[1] == 'AND':
                if query_tokens[0] == 'NOT':
                    return self.and_not_op(list(postings[1].values())[0], list(postings[0].values())[0])
                elif query_tokens[2] == 'NOT':
                    return self.and_not_op(list(postings[0].values())[0], list(postings[1].values())[0])
                return self.and_op(list(postings[0].values())[0], list(postings[1].values())[0])
            elif query_tokens[1] == 'OR':
                if query_tokens[0] == 'NOT':
                    return self.or_not_op(list(postings[1].values())[0], list(postings[0].values())[0])
                elif query_tokens[2] == 'NOT':
                    return self.or_not_op(list(postings[0].values())[0], list(postings[1].values())[0])
                return self.or_op(list(postings[0].values())[0], list(postings[1].values())[0])
        else:
            # recursively evaluate the query
            if query_tokens[1] == 'AND':
                return self.and_op(list(postings[0].values())[0], self.evaluate_query([postings[1], postings[2]], query_tokens[2:]))
            elif query_tokens[1] == 'OR':
                return self.or_op(list(postings[0].values())[0], self.evaluate_query([postings[1], postings[2]], query_tokens[2:]))
            else:
                self.error_logger.error(f"Invalid query: {query_tokens}")
                return []
                
    def and_op(self, p1: List[int], p2: List[int]) -> List[int]:
        p1 = set(p1)
        p2 = set(p2)
        return list(p1.intersection(p2))
    
    def or_op(self, p1: List[int], p2: List[int]) -> List[int]:
        p1 = set(p1)
        p2 = set(p2)
        return list(p1.union(p2))
    
    def not_op(self, p1: List[int]):
        p1 = set(p1)
        return list(set(self.all_docs).difference(p1))
    
    def and_not_op(self, p1: List[int], p2: List[int]) -> List[int]:
        p1 = set(p1)
        p2 = set(p2)
        return list(p1.difference(p2))
    
    def or_not_op(self, p1: List[int], p2: List[int]) -> List[int]:
        p1 = set(p1)
        p2 = set(p2)
        return list(set(p1).union(set(self.all_docs).difference(p2)))
    
   
    def remove_duplicate_not(self, tokens):
        # Remove duplicate occurrences of "NOT"
        unique_tokens = [tokens[0]]
        for i in range(1, len(tokens)):
            if tokens[i] == 'NOT' and tokens[i - 1] == 'NOT':
                continue
            unique_tokens.append(tokens[i])
        return unique_tokens

    def get_postings(self, words: List[str]):
        postings = []
        for word in words:
            if word in self.inv_idx:
                # sort the documents in terms of frequency of the word
                # docs = sorted(self.inv_idx[word].items(), key=lambda x: x[1], reverse=False)
                docs = list(self.inv_idx[word].keys())
                # docs = [(doc.split('_')[1]) for doc in docs]
                docs = [int(doc.split('_')[1]) for doc in docs]
                docs.sort()
                postings.append({word: docs})
            else:
                self.error_logger.error(f"Word '{word}' not found in inverted index")
        return postings

if __name__=="__main__":
    bm = BooleanModel()
    query = "cancer AND learning"
    docs = bm.process_query(query)
    print(docs)
