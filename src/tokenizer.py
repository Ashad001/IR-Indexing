import re

class Tokenizer:
    def __init__(self, text: str, stop_words_file_path: str='../data/Stopword-List.txt') -> None:
        self.text: str = text
        self.stop_words: list = []
        self.load_stop_words(stop_words_file_path)
        self.tokens = self.tokenize()
        
        
    def load_stop_words(self, file_path: str) -> None:
        with open(file_path, 'r', encoding='utf-8') as file:
            stop_words = file.read().split('\n')
        self.stop_words = [word.strip() for word in stop_words]
            
    def tokenize(self) -> list:
        tokens = re.findall(r'\b\w+\b', self.text)
        return [token.lower() for token in tokens if token.lower() not in self.stop_words]
    