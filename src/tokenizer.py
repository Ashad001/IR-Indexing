import re
from typing import List, Any, Tuple, Dict
from porter_stemmer import PorterStemmer

# https://regex101.com/

class Tokenizer:
    def __init__(self, stop_words_file_path: str = "../data/Stopword-List.txt") -> None:
        """
        Args:
            stop_words_file_path (str, optional): . Defaults to '../data/Stopword-List.txt'.
        """
        self.stop_words: List[str] = []
        self.load_stop_words(stop_words_file_path)
        self.stemmer = PorterStemmer()

    def is_number(self, s) -> bool:
        """
        Returns True if s is a number

        Args:
            s (_type_): word to be checked

        Returns:
            bool: True/False 
        """
        try:
            float(s)
            return True
        except ValueError:
            return False

    def has_number(self, s: str)-> bool:
        """
        Returns True if string s contains a digit

        Args:
            s (str): word to check

        Returns:
            bool: True/false 
        """
        return bool(re.search(r'\d', s))

    def load_stop_words(self, file_path: str) -> None:
        """
        Loads stop words and store in stop_words

        Args:
            file_path (str): file_path for stop words
        """
        with open(file_path, "r", encoding="utf-8") as file:
            stop_words = file.read().split("\n")
        self.stop_words = [word.strip() for word in stop_words]
        
    def preprocess(self, text: str) -> str:
        """
        Preprocess the text to remove special characters

        Args:
            text (str): text to be preprocessed

        Returns:
            str: preprocessed text
        """
        cleaned_text =  text.encode('ascii', 'ignore').decode()
        cleaned_text = re.sub(r'\d', "", cleaned_text)
        return cleaned_text

    def tokenize_text(self, text: str) -> Tuple[List[str], Dict[str, int]]:
        """
        Tokenize the text (English words; ignore numbers)
        
        Args:
        text (str): Extracted English text (with numbers)
        
        Returns:
        Tuple[List[str], Dict[str, str]]: Tuple containing two lists - dictionary tokens and stemmed tokens
        """ 
        cleaned_text = self.preprocess(text )
        tokens: List[str] = re.findall(r"\b\w+\b", cleaned_text)
        dict_tokens: Dict[str, int] = {}
        stemmed_tokens: List[str] = []

        for token in tokens:
            if token.lower() not in self.stop_words and not self.is_number(token):
                stemmed_token = self.stemmer.stem(token.strip())
                if token in dict_tokens and not self.has_number(token):
                    dict_tokens[token] += 1
                else:
                    dict_tokens[token] = 1
                stemmed_tokens.append(stemmed_token)

        dict_tokens = sorted(dict_tokens.items(), key=lambda x: x[0])
        
        return dict_tokens, stemmed_tokens
    
    def tokenize(self, text: str) -> List[str]:
        """
        Tokenize the text (English words; ignore numbers)
        
        Args:
        text (str): Extracted English text (with numbers)
        
        Returns:
        List[str]: Preprocessed and tokenized text
        """ 
        cleaned_text = self.preprocess(text )
        tokens: List[str] = re.findall(r"\b\w+\b", cleaned_text)

        return tokens



