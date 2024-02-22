import os
import json
from tokenizer import Tokenizer
from porter_stemmer import PorterStemmer
from inverted_index import InvertedIndex
from positional_index import PositionalIndex
from typing import List, Tuple, Dict, Optional

def read_data(file_name: str) -> List[str]:
    """
    reads data from file

    Args:
        file_name (str): file name
    """
    with open(file_name, 'r') as file:
        data = file.read()
    return data

def main(data_dir: str) -> None:
    """
    reads data from directory and makes positional and inverted index

    Args:cls
        data_dir (str): data directory path
    """
    inv_idx = InvertedIndex()
    pos_idx = PositionalIndex()
    files: List[str] = os.listdir(data_dir)
    
    for file in files:
        if file.endswith('.txt'):
            data = read_data(os.path.join(data_dir, file))
            tokens = Tokenizer(data).tokens
            stemmed_tokens = [PorterStemmer().stem(token.strip()) for token in tokens]
            inv_idx.add_to_index(file_name=file, tokens=stemmed_tokens)
            pos_idx.add_to_index(file_name=file, tokens=stemmed_tokens)
    
    with open("test_inv-index.json", 'w', encoding='utf-8') as f:
        json.dump(inv_idx.index, f, indent=4)
    with open("test_pos-index.json", 'w', encoding='utf-8') as f:
        json.dump(pos_idx.index, f, indent=4)
        
if __name__=="__main__":
    main("../data/ResearchPapers/")
    