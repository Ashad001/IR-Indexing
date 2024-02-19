import unittest
from src.porter_stemmer import PorterStemmer

class TestPorterStemming(unittest.TestCase):
    def setUp(self):
        # Mock data for testing
        self.tokens = ['running', 'jumps', 'quickly', 'houses', 'easily', 'friendship', 'agreed', 'tiredly']

    def test_porter_stemming(self):
        porter = PorterStemmer()
        expected_stems = ['run', 'jump', 'quickli', 'hous', 'easili', 'friendship', 'agre', 'tire']
        actual_stems = [porter(token) for token in self.tokens]
        self.assertEqual(actual_stems, expected_stems)

if __name__ == '__main__':
    unittest.main()
