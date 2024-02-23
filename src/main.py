import os
import re
import json
import json

from tokenizer import Tokenizer
from porter_stemmer import PorterStemmer
from inverted_index import InvertedIndex
from positional_index import PositionalIndex
from utils import log_message, get_logger, metadata_lookup

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
        
    metadata_logger = get_logger("metadata")
    lookup_logger = get_logger("lookup", see_time=True)
    
    for file in files:
        if file.endswith('.txt'):
            data: str = read_data(os.path.join(data_dir, file))
            doc_id: str = re.findall(r'\d+', file)[0] + data[:10] # Has to be unique
            
            tokens: List[str] = Tokenizer(data).tokens
            stemmed_tokens: List[str] = [PorterStemmer().stem(token.strip()) for token in tokens]
            
            metadata = {
                "doc_id": doc_id,
                "tokens": len(tokens),
                "stemmed_tokens": len(stemmed_tokens)
            }    
            
            if metadata_lookup(metadata, "metadata", logger=lookup_logger):
                continue
            
            log_message(json.dumps(metadata, indent=4), logger=metadata_logger)            
            
            inv_idx.add_to_index(doc_id=doc_id, tokens=stemmed_tokens)
            pos_idx.add_to_index(doc_id=doc_id, tokens=stemmed_tokens)
            
    with open("test_inv-index.json", 'w', encoding='utf-8') as f:
        json.dump(inv_idx.index, f, indent=4)
    with open("test_pos-index.json", 'w', encoding='utf-8') as f:
        json.dump(pos_idx.index, f, indent=4)
        
if __name__=="__main__":
    main("../data/ResearchPapers/")
    