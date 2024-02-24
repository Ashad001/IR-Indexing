import re
from typing import List, Any
from porter_stemmer import PorterStemmer


class Tokenizer:
    def __init__(self, stop_words_file_path: str = "../data/Stopword-List.txt") -> None:
        """
        Args:
            stop_words_file_path (str, optional): . Defaults to '../data/Stopword-List.txt'.
        """
        self.stop_words: List[str] = []
        self.load_stop_words(stop_words_file_path)
        self.stemmer = PorterStemmer()

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
        with open(file_path, "r", encoding="utf-8") as file:
            stop_words = file.read().split("\n")
        self.stop_words = [word.strip() for word in stop_words]

    def tokenize(self, text: str) -> List[Any]:
        """
        Tokinze the text (english words; in words)
        
        Args:
        text (str): extracted english text (with numbers)
        Returns:
            list: token list after stemming, removing stop words and ignoring numbers
        """

        tokens: List[Any] = re.findall(r"\b\w+\b", text)
        return [
            self.stemmer.stem(token.strip())
            for token in tokens
            if token.lower() not in self.stop_words and not self.is_number(token)
        ]
