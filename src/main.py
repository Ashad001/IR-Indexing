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

# TODO: Fix Tokenizer
# TODO: Fix Data Pass
# TODO: Fix Index Loading and Saving
# TODO: Add Dicitonary Index For Spell Checkers

INDEX_FILES = 'indexes'

def read_data(file_name: str) -> List[str]:
    """
    reads data from file

    Args:
        file_name (str): file name
    """
    with open(file_name, 'r') as file:
        data = file.read()
    return data

def write_data(file_name: str, data: Dict[str, Dict[str, List[int]]]) -> None:
    """
    writes data to file

    Args:
        file_name (str): file name
        data (List[str]): data to write
    """
    with open(file_name, 'w') as file:
        json.dump(data, file, indent=4)
        

def main(data_dir: str) -> None:
    """
    reads data from directory and makes positional and inverted index

    Args:cls
        data_dir (str): data directory path
    """
    inv_idx: Dict[str, Dict[str, List[int]]] = {}
    pos_idx: Dict[str, Dict[str, List[int]]] = {}
    dict_set: Dict[str, int] = {}
    files: List[str] = os.listdir(data_dir)
    
    
    
    metadata_logger = get_logger("metadata")
    lookup_logger = get_logger("lookup", see_time=True)
    error_logger = get_logger("error", see_time=True)
    
    index_dir = './' + INDEX_FILES
    os.makedirs(index_dir, exist_ok=True)
    
    file_iter = 1
    for file in files:
        if file.endswith('.txt'):
            data: str = read_data(os.path.join(data_dir, file))
            doc_id: str = re.findall(r'\d+', file)[0] # + data[:10] # Has to be unique
            doc_id = str(file_iter) + "_" + doc_id   # This way, we don't need to sort the postings and can get document ids after _ directly.
            file_iter += 1

            dict_tokens:  Dict[str, int]
            stemmed_tokens: List[str]
            dict_tokens, stemmed_tokens = Tokenizer().tokenize(data)
            
            
            local_inv_idx = InvertedIndex()
            local_pos_idx = PositionalIndex()
            
            metadata = {
                "doc_id": doc_id,
                "unique_tokens": len(dict_tokens),
                "stemmed_tokens": len(stemmed_tokens)
            }    
            
            inv_index_file = os.path.join(index_dir, f"{doc_id}_ivnIdx.json")
            pos_index_file = os.path.join(index_dir, f"{doc_id}_posIdx.json")
               
            if metadata_lookup(metadata, "metadata", logger=lookup_logger):
                local_inv_idx.load_from_index(inv_index_file, logger=error_logger)
                local_pos_idx.load_from_index(pos_index_file, logger=error_logger)
                
                inv_idx.update(local_inv_idx.index)
                pos_idx.update(local_pos_idx.index)
                dict_set.update(dict_tokens)            
                continue
            
            log_message(json.dumps(metadata, indent=4), logger=metadata_logger)            
            
            local_inv_idx.add_to_index(doc_id=doc_id, tokens=stemmed_tokens)
            local_pos_idx.add_to_index(doc_id=doc_id, tokens=stemmed_tokens)
            
            write_data(inv_index_file, local_inv_idx.index)
            write_data(pos_index_file, local_pos_idx.index)
            
            inv_idx.update(local_inv_idx.index)
            pos_idx.update(local_pos_idx.index)
            
            dict_set.update(dict_tokens)
            
    with open("test_inv-index.json", 'w', encoding='utf-8') as f:
        json.dump(inv_idx, f, indent=4)
    with open("test_pos-index.json", 'w', encoding='utf-8') as f:
        json.dump(pos_idx, f, indent=4)
    with open("test_dict-set.json", 'w', encoding='utf-8') as f:
        json.dump(dict_set, f, indent=4)
        
if __name__=="__main__":
    main("../data/ResearchPapers/")
    