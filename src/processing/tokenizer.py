import os
import re
import math
from typing import List, Tuple, Dict
from src.processing.porter_stemmer import PorterStemmer

# https://regex101.com/

class Tokenizer:
    def __init__(self, stop_words_file_path: str = "./data/Stopword-List.txt") -> None:
        """
        Args:
            stop_words_file_path (str, optional): . Defaults to '../data/Stopword-List.txt'.
        """
        self.stop_words: List[str] = []
        self.stemmer = PorterStemmer()

        self.load_stop_words(stop_words_file_path)

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
    
    def get_pattern(self) -> str:
        """
        Returns a regex pattern to match a word

        Returns:
            str: regex pattern
        """
        return r"\b\w+\b"

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
        self.stop_words = [word.strip() for word in stop_words if word.strip() != ""]
    
    def remove_stop_words(self, text: str) -> str:
        """
        Removes stop words from the text

        Args:
            text (str): text to be processed

        Returns:
            str: processed text
        """
        return " ".join([word for word in text.split(' ') if word not in self.stop_words])    
    
    def split_string_by_sqrt(self, string: str) -> List[str]:
        """
        Splits the input string into a list of substrings, where each substring's length
        is determined by the square root of the length of the input string if it is greater
        than 12. If the input string is 12 characters or shorter, it returns a list
        containing the original string.

        Args:
            string (str): The input string to be split.

        Returns:
            List[str]: A list of substrings.
        """
        if len(string) > 12:
            split_length = int(math.sqrt(len(string)))
            result_list = [string[i:i + split_length] for i in range(0, len(string), split_length)]
            return result_list
        else:
            return [string]

        
    def preprocess(self, token: str, case_fold=True) -> List[str]:
        """
        Preprocess the text to remove special characters

        Args:
            text (str): text to be preprocessed

        Returns:
            str: preprocessed text
        """
        if case_fold:
            token = token.lower()
            if len(token) > 24 or len(token) < 2 or token in self.stop_words or self.is_number(token):
                return ""
                
        token = token.encode('ascii', 'ignore').decode()
        if self.has_number(token) and not self.is_number(token):
            token = self.replace_numbers(token)
        token = self.unicode_remover(token)
        
        return token

    def replace_numbers(self, text: str) -> str:
        """
        Replace numbers in the text with the word "number"

        Args:
            text (str): text to be processed

        Returns:
            str: processed text
        """
        return re.sub(r"\d+", "", text)
    
    def unicode_remover(self, text: str) -> str:
        """
        Remove unicode characters from the text

        Args:
            text (str): any text or word or token

        Returns:
            str: 
        """
        pattern = r"\\u[\dA-Fa-f]{4}"
        return re.sub(pattern, "", text)
    
    def tokenize(self, text: str, case_fold=True) -> List[str]:
        """
        Tokenize the text (English words; ignore numbers)
        
        Args:
        text (str): Extracted English text (with numbers)
        
        Returns:
        List[str]: Preprocessed and tokenized text
        """ 
        tokens: List[str] = []
        for word in re.findall(r"\b\w+\b", text):
            token = self.preprocess(word, case_fold=case_fold)
            if token != "":
                tokens.append(token)

        return tokens

if __name__ == "__main__":
    tk = Tokenizer()
    print(tk.split_string_by_sqrt("desenvolvimentocientficoetecnolgicoabstract"))