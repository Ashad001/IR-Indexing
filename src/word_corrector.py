import re
import json
from typing import List, Dict


# used dynamic programming to find the minimum distance between two words i.e. lavenstein distance
class WordCorrector:
    def __init__(self, dictionary: Dict[str, int]) -> None:
        self.dictionary: List[str] = dictionary.keys()
        
    def word_corrector(self, word: str) -> str:
        """
        Corrects the word and returns the corrected word
        
        Args:
            word (str): word to be corrected
        
        Returns:
            str: corrected word
        """
        word = word.lower()
        if word in self.dictionary:
            return word
        else:
            min_distance = float('inf')
            corrected_word = word
            for dict_word in self.dictionary:
                distance = self.lavenstein_distance(word, dict_word)
                if distance < min_distance:
                    min_distance = distance
                    corrected_word = dict_word
            return corrected_word
        
    def lavenstein_distance(self, word: str, word_dict: str) -> int:
        """
        Find the minimum distance between two words
        
        Args:
            word (str): word 1
            word_dict (str): word 2
            
        Returns:
            int: minimum distance between the two words
        """
        m = len(word)
        n = len(word_dict)
        dp = [[0 for _ in range(n + 1)] for _ in range(m + 1)]
        
        for i in range(m + 1):
            for j in range(n + 1):
                if i == 0:
                    dp[i][j] = j
                elif j == 0:
                    dp[i][j] = i
                elif word[i - 1] == word_dict[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    dp[i][j] = 1 + min(dp[i][j - 1], dp[i - 1][j], dp[i - 1][j - 1])
        return dp[m][n]
    
    def correct_query(self, query: str) -> str:
        """
        Corrects the query and returns the corrected query
        
        Args:
            query (str): query to be corrected
        
        Returns:
            str: corrected query
        """
        words = query.split()
        corrected_query = ""
        for word in words:
            if word not in ['AND', 'OR', "NOT"] and re.search(r'/\d+$/', word):
                corrected_query += word + " "
            else:
                corrected_query += self.word_corrector(word) + " "
        return corrected_query.strip()