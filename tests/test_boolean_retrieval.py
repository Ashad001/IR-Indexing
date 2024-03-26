import unittest
import os
from src.models.boolean_model import BooleanModel
from src.processing.processor import IndexProcessor
from src.utils import list_files

class TestBooleanModel(unittest.TestCase):
    def test_search(self) -> None:
        index_processor = IndexProcessor("./data", exclude_files=['Stopword-List.txt'])
        inv_idx, _, _ = index_processor.process_data()
        queries, results = self.load_tests("./tests/test_sets/golden_boolean_queries.txt")
        all_docs = list_files('./data', exclude_files=['Stopword-List.txt'])
        boolean_model = BooleanModel(inv_idx=inv_idx.index, all_docs=all_docs)
        for query, result in zip(queries, results):
            result = set(result.split(", "))  
            docs = set(boolean_model.search(query))
            self.assertEqual(set(docs), result)  
    
    def load_tests(self, test_file: str):
        queries = []
        results = []
        try:
            with open(test_file, 'r') as f:
                test_cases = f.readlines()
            test_cases = [test_case.strip() for test_case in test_cases]
            test_cases = list(filter(lambda x: x != "", test_cases))
            
            for line in test_cases:
                if "example query" in line.lower():
                    line = line.replace("Example Query: ", "")
                    queries.append(line)
                if "result-set" in line.lower():
                    line = line.replace("Result-Set: ", "")
                    results.append(line)
                    
        except Exception as e:
            print(f"Error occurred while loading tests: {e}")
        
        return queries, results
    
        