import os
import json
from typing import List, Dict, Union
from src.utils import time_logger

class TrieNode:
    def __init__(self):
        """Initialize a TrieNode."""
        self.children: Dict[str, TrieNode] = {}
        self.is_end_of_word: bool = False

class WordSuggestor:
    def __init__(self, dictionary_set: Dict[str, int]):
        """Initialize WordCorrector with a dictionary file."""
        self.data: Dict[str, str|int] = dictionary_set
        self.trie: TrieNode = self.build_trie(dictionary_set)

    def load_dictionary(self, file_path: str) -> List[str]:
        """
        Load a dictionary from a file.

        Args:
            file_path (str): The path to the dictionary file.

        Returns:
            List[str]: List of words loaded from the dictionary file.
        """
        with open(file_path, 'r') as f:
            self.data = json.load(f)
        return [word for word in self.data.keys()]

    @time_logger
    def build_trie(self, words: List[str]) -> TrieNode:
        """
        Build a Trie data structure from a list of words.

        Args:
            words (List[str]): List of words to build the Trie from.

        Returns:
            TrieNode: The root of the Trie.
        """
        root = TrieNode()
        for word in words:
            node = root
            for char in word:
                if char not in node.children:
                    node.children[char] = TrieNode()
                node = node.children[char]
            node.is_end_of_word = True
        return root

    def suggest_words(self, prefix: str) -> List[str]:
        """
        Get a list of word suggestions for a given prefix.

        Args:
            prefix (str): The prefix to search for.

        Returns:
            List[str]: List of suggested words.
        """
        node = self.trie
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]

        suggestions = []
        self.find_words_with_prefix(node, prefix, suggestions)
        return suggestions

    def find_words_with_prefix(self, node: TrieNode, current_word: str, suggestions: List[str]) -> None:
        """
        Recursively find words with a given prefix in the Trie.

        Args:
            node (TrieNode): Current Trie node.
            current_word (str): Current word being constructed.
            suggestions (List[str]): List to store suggestions.
        """
        if node.is_end_of_word:
            suggestions.append(current_word)

        for char, child_node in node.children.items():
            self.find_words_with_prefix(child_node, current_word + char, suggestions)

    @time_logger
    def find_words(self, word: str) -> List[Dict[str, Union[str, int]]]:
        """
        Find words in the dictionary based on a given input word

        Args:
            word (str): The input word.

        Returns:
            List[Dict[str, str|int]: List of dictionaries containing suggested words and their orrcurence.
        """
        suggestions = self.suggest_words(word)
        priority_suggestions = {}
        for suggestion in suggestions:
            if suggestion in self.data:
                priority_suggestions[suggestion] = self.data[suggestion]

        # sort dict by values
        priority_suggestions = sorted(priority_suggestions.items(), key=lambda x: x[1], reverse=True)
        # return only suggestions, not occurendces
        priority_suggestions = [suggestion[0] for suggestion in priority_suggestions]

        return priority_suggestions[:8]
    

if __name__ =="__main__":
    
    dictionary_file = '../docs/dict-set.json'
    with open(dictionary_file, 'r') as f:
        dictionary = json.load(f)
    word_corrector = WordSuggestor(dictionary)

    input_word = "intel"
    print(word_corrector.find_words(input_word))
