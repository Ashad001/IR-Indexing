import re
import json
from typing import List, Dict
from src.porter_stemmer import PorterStemmer as Stemmer
from src.tokenizer import Tokenizer
from src.utils import get_logger, timing_decorator, log_message, CONSOLE_LOGS
import os



class BooleanModel:
    def __init__(self, inv_idx: Dict[str, Dict[str, List[int]]], all_docs_files: List[int]) -> None:
        self.inv_idx: Dict[str, Dict[str, List[int]]] = inv_idx
        all_docs = []
        for file in all_docs_files:
            doc_id = re.findall(r'[^\\/]*$', file)
            doc_id = doc_id[0].split(".")[0]
            all_docs.append(doc_id)
        self.all_docs = all_docs
        self.stemmer = Stemmer()
        self.tokenizer = Tokenizer()
        self.logger = get_logger("boolean_model", see_time=True, console_log=CONSOLE_LOGS)
        self.error_logger = get_logger("boolean_model_error", see_time=True, console_log=CONSOLE_LOGS)
    
    @timing_decorator
    def search(self, query: str) -> List[str]:
        """
        Main Process Query function that processes the query and returns the documents that satisfy the query

        Args:
            query (str): user query of the form "word1 AND word2 OR word3 NOT word4"

        Returns:
            List[str]: documents that satisfy the query
        """
        tokens: List[str] = self.tokenizer.tokenize(query)
        words: List[str] = [self.stemmer.stem(word.lower()) for word in tokens if word.upper() not in ['AND', 'OR', 'NOT']]
        postings: Dict[str, List[int]] = self.get_postings(words)
        if re.search(r'^(?!.*\b(?:OR|NOT)\b).*\bAND\b.*', query):
            # sort posrings by assending order if only AND is present
            postings = sorted(postings, key=lambda x: len(list(x.values())[0]), reverse=True)
        if len(postings) == 0:
            return []
        documents: List[int|str] = self.evaluate_query(postings, tokens)
        documents: List[int] = [doc for doc in documents]
        # log docs
        log_message(json.dumps({"query": query, "documents": documents}, indent=4), self.logger)
        return documents

    
    def evaluate_query(self, postings: List[Dict[str, List[int]]], query_tokens: List[str]) -> List[int]: 
        """
        REcursively Evaluate the query using the postings list and the query tokens

        Args:
            postings (List[Dict[str, List[int]]]): postings list for the words in the query
            query_tokens (List[str]): all the tokens in the query

        Returns:
            List[int]: documents that satisfy the query (recursively evaluated)
        """
        
        if len(postings) == 1:
            if query_tokens[0] == 'NOT':
                return self.not_op(list(postings[0].values())[0])
            return list(postings[0].values())[0]
        elif len(postings) == 2:
            if query_tokens[0] == "NOT": 
                return self.not_op(self.evaluate_query(postings[:1], query_tokens[1:]))
            if query_tokens[1] == 'AND':
                if query_tokens[0] == 'NOT':
                    return self.and_not_op(list(postings[1].values())[0], list(postings[0].values())[0])
                elif query_tokens[2] == 'NOT':
                    return self.and_not_op(list(postings[0].values())[0], list(postings[1].values())[0])
                return self.and_op(list(postings[0].values())[0], list(postings[1].values())[0])
            elif query_tokens[1] == "OR":
                if query_tokens[0] == 'NOT':
                    return self.or_not_op(list(postings[1].values())[0], list(postings[0].values())[0])
                elif query_tokens[2] == 'NOT':
                    return self.or_not_op(list(postings[0].values())[0], list(postings[1].values())[0])
                return self.or_op(list(postings[0].values())[0], list(postings[1].values())[0])
        else:
            #* recursively evaluate the query..!
            if query_tokens[0] == 'NOT':
                return self.not_op(self.evaluate_query([postings[0]], query_tokens[1:]))
            if query_tokens[1] == 'AND':
                if query_tokens[2] == 'NOT':
                    return self.and_not_op(list(postings[0].values())[0], self.evaluate_query([postings[1], postings[2]], query_tokens[3:]))
                return self.and_op(list(postings[0].values())[0], self.evaluate_query([postings[1], postings[2]], query_tokens[2:]))
            elif query_tokens[1] == 'OR':
                if query_tokens[2] == 'NOT':
                    return self.or_not_op(list(postings[0].values())[0], self.evaluate_query([postings[1], postings[2]], query_tokens[3:]))
                return self.or_op(list(postings[0].values())[0], self.evaluate_query([postings[1], postings[2]], query_tokens[2:]))
            else:
                log_message(f"Invalid query: {query_tokens}", self.error_logger, console_log=CONSOLE_LOGS)
                self.error_logger.error(f"Invalid query: {query_tokens}")
                return []
                
    def and_op(self, p1: List[int], p2: List[int]) -> List[int]:
        """
        Perform AND operation on the two postings list

        Args:
            p1 (List[int]): word1's postings list
            p2 (List[int]): word2's postings list

        Returns:
            List[int]: word1 AND word2's postings list
        """
        p1 = set(p1)
        p2 = set(p2)
        return list(p1.intersection(p2))
    
    def or_op(self, p1: List[int], p2: List[int]) -> List[int]:
        """
        Perform OR operation on the two postings list

        Args:
            p1 (List[int]): word1's postings list
            p2 (List[int]): word2's postings list

        Returns:
            List[int]: word1 OR word2's postings list
        """
        p1 = set(p1)
        p2 = set(p2)
        return list(p1.union(p2))
    
    def not_op(self, p1: List[int]):
        """
        Perform NOT operation on the postings list

        Args:
            p1 (List[int]): word1's postings list

        Returns:
            _type_: word1's NOT postings list
        """
        p1 = set(p1)
        return list(set(self.all_docs).difference(p1))
    
    def and_not_op(self, p1: List[int], p2: List[int]) -> List[int]:
        p1 = set(p1)
        p2 = set(p2)
        return list(p1.intersection(self.not_op(p2)))
        # return list(p1.difference(p2))
    
    def or_not_op(self, p1: List[int], p2: List[int]) -> List[int]:
        p1 = set(p1)
        p2 = set(p2)
        return list(p1.union(self.not_op(p2)))
        # return list(set(p1).union(set(self.all_docs).difference(p2)))
    

    def get_postings(self, words: List[str]) -> Dict[str, List[int]]:
        """
        Generate the postings list for the words in the query

        Args:
            words (List[str]): words in the query

        Returns:
            Dict[str, List[int]]: word and its corresponding postings list
        """
        postings = []
        for word in words:
            try:
                if word in self.inv_idx:
                    docs = list(self.inv_idx[word].keys())
                    # docs = [(doc.split('_')[1]) for doc in docs]
                    docs = [doc.split('_')[1] for doc in docs]
                    docs.sort()
                    postings.append({word: docs})
                else:
                    postings.append({word: []})
                    self.error_logger.error(f"Word '{word}' not found in inverted index")
            except Exception as e:
                self.error_logger.error(f"Error occurred while processing word '{word}': {str(e)}")
                postings.append({word: []})
        return postings

if __name__=="__main__":
    all_docs = os.listdir('../data/ResearchPapers')
    with open(f'../docs/inv-index.json', 'r') as f:    
        inv_idx = json.load(f)
    bm = BooleanModel(inv_idx, all_docs=all_docs)
    queries = [
        "transformer AND NOT heart OR NOT artificial OR intelligence",
        "transformer",
        "NOT heart",
        "transformer AND NOT",
        "NOT artificial",
        "intelligence",
    ]
    
    for query in queries:
        docs = bm.search(query)
        print(docs)
