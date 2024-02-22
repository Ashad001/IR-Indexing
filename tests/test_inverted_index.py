import unittest
from src.inverted_index import InvertedIndex

class TestInvertedIndex(unittest.TestCase):
    def test_add_to_index(self) -> None:
        inv_idx = InvertedIndex()
        inv_idx.add_to_index("1.txt", ["hello", "ashad"])
        self.assertEqual(inv_idx.index, {'hello': {'1.txt': 1}, 'ashad': {'1.txt': 1}})
        
        inv_idx.add_to_index("2.txt", ["hello", "ashad"])
        self.assertEqual(inv_idx.index, {'hello': {'1.txt': 1, '2.txt': 1}, 'ashad': {'1.txt': 1, '2.txt': 1}})
        
        inv_idx.add_to_index("3.txt", ["hello", "ashad", "ashad"])
        self.assertEqual(inv_idx.index, {'hello': {'1.txt': 1, '2.txt': 1, '3.txt': 1}, 'ashad': {'1.txt': 1, '2.txt': 1, '3.txt': 2}})
        
        inv_idx.add_to_index("4.txt", ["hello", "ashad", "ashad", "ashad"])
        self.assertEqual(inv_idx.index, {'hello': {'1.txt': 1, '2.txt': 1, '3.txt': 1, '4.txt': 1}, 'ashad': {'1.txt': 1, '2.txt': 1, '3.txt': 2, '4.txt': 3}})
        
        inv_idx.add_to_index("5.txt", ["hello", "ashad", "ashad", "ashad", "ashad"])
        self.assertEqual(inv_idx.index, {'hello': {'1.txt': 1, '2.txt': 1, '3.txt': 1, '4.txt': 1, '5.txt': 1}, 'ashad': {'1.txt': 1, '2.txt': 1, '3.txt': 2, '4.txt': 3, '5.txt': 4}})
                
        
if __name__=="__main__":
    unittest.main()
