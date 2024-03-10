import unittest
from src.inverted_index import InvertedIndex

class TestInvertedIndex(unittest.TestCase):
    def test_add_to_index(self) -> None:
        inv_idx = InvertedIndex()
        inv_idx.add_to_index("1", "hello")
        inv_idx.add_to_index("1", "ashad")
        self.assertEqual(inv_idx.index, {'hello': {'1': 1}, 'ashad': {'1': 1}})
        
        inv_idx.add_to_index("2", "hello")
        inv_idx.add_to_index("2", "ashad")
        self.assertEqual(inv_idx.index, {'hello': {'1': 1, '2': 1}, 'ashad': {'1': 1, '2': 1}})
        
        inv_idx.add_to_index("3", "hello")
        inv_idx.add_to_index("3", "ashad")
        inv_idx.add_to_index("3", "ashad")
        self.assertEqual(inv_idx.index, {'hello': {'1': 1, '2': 1, '3': 1}, 'ashad': {'1': 1, '2': 1, '3': 2}})
        
        inv_idx.add_to_index("4", "hello")
        inv_idx.add_to_index("4", "ashad")
        inv_idx.add_to_index("4", "ashad")        
        inv_idx.add_to_index("4", "ashad")                        
        self.assertEqual(inv_idx.index, {'hello': {'1': 1, '2': 1, '3': 1, '4': 1}, 'ashad': {'1': 1, '2': 1, '3': 2, '4': 3}})
        
        inv_idx.add_to_index("5", "hello")
        inv_idx.add_to_index("5", "ashad")
        inv_idx.add_to_index("5", "ashad")
        inv_idx.add_to_index("5", "ashad")
        inv_idx.add_to_index("5", "ashad")
        self.assertEqual(inv_idx.index, {'hello': {'1': 1, '2': 1, '3': 1, '4': 1, '5': 1}, 'ashad': {'1': 1, '2': 1, '3': 2, '4': 3, '5': 4}})
                
        
if __name__=="__main__":
    unittest.main()
