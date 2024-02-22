import re
from typing import List, Any
class Tokenizer:
    def __init__(self, text: str, stop_words_file_path: str='../data/Stopword-List.txt') -> None:
        """
        Args:
            text (str): extracted english text (with numbers)
            stop_words_file_path (str, optional): . Defaults to '../data/Stopword-List.txt'.
        """
        
        self.text: str = text
        self.stop_words: List[str] = []
        self.load_stop_words(stop_words_file_path)
        self.tokens = self.tokenize()
    
    def is_number(self, s):
        try:
            float(s)
            return True
        except ValueError:
            return False
        
        
    def load_stop_words(self, file_path: str) -> None:
        """
        Loads stop words and store in stop_words
        
        Args:
            file_path (str): file_path for stop words
        """
        with open(file_path, 'r', encoding='utf-8') as file:
            stop_words = file.read().split('\n')
        self.stop_words = [word.strip() for word in stop_words]
            
    def tokenize(self) -> List[Any]:
        """
        Tokinze the text (english words; in words)

        Returns:
            list: token list
        """
        tokens: List[Any] = re.findall(r'\b\w+\b', self.text)
        return [token for token in tokens if token.lower() not in self.stop_words and not self.is_number(token)]
    