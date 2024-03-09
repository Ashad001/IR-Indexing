import os
import re
import json
import json

from src.tokenizer import Tokenizer
from src.porter_stemmer import PorterStemmer

from src.inverted_index import InvertedIndex
from src.positional_index import PositionalIndex

from src.utils import *

from typing import List, Dict

# TODO: Fix Data Pass

INDEX_FILES = "indexes"
VOCAB_FILES = "vocab"

@timing_decorator
def processor(data_dir: str, exclude_files: List[str] = ["Stopword-List.txt"]) -> None:
    """
    reads data from directory and makes positional and inverted index

    Args:cls
        data_dir (str): data directory path
    """
    inv_idx = InvertedIndex()
    pos_idx = PositionalIndex()
    dict_set: Dict[str, int] = {}

    tokenizer = Tokenizer()
    stemmer = PorterStemmer()

    files: List[str] = list_files(data_dir, exclude_files)

    metadata_logger = get_logger("metadata", see_time=False, console_log=False, level=logging.INFO)
    lookup_logger = get_logger("lookup", see_time=True, console_log=False, level=logging.INFO)
    error_logger = get_logger("processor_error", see_time=True, console_log=CONSOLE_LOGS, level=logging.ERROR)

    index_dir = "./src/" + INDEX_FILES
    vocab_file = "./src/" + VOCAB_FILES
    
    os.makedirs(index_dir, exist_ok=True)
    os.makedirs(vocab_file, exist_ok=True)

    logged_metadata = read_metadata("metadata")

    file_iter = 1
    for file in files:
        if file.endswith(".txt"):
            data: str = read_data( file)
            doc_id: str = re.findall(r"\d+", file)[0]  # + data[:10] # Has to be unique
            doc_id = (
                str(file_iter) + "_" + doc_id
            )  # This way, we don't need to sort the postings and can get document ids after _ directly.
            file_iter += 1

            stemmed_tokens: List[str] = []
            # dict_tokens, stemmed_tokens = Tokenizer().tokenize_text(data)
            # tokens = tokenizer.tokenize(data)

            local_inv_idx = InvertedIndex()
            local_pos_idx = PositionalIndex()
            local_dict: Dict[str, int] = {}
            token_length = 0

            metadata = {
                "doc_id": doc_id,
                # "tokens": len(tokens),
            }

            inv_index_file = os.path.join(index_dir, f"{doc_id}_ivnIdx.json")
            pos_index_file = os.path.join(index_dir, f"{doc_id}_posIdx.json")
            vocab_dict_file = os.path.join(vocab_file, f"{doc_id}_vocab.json")

            if metadata_lookup(metadata, logged_metadata, logger=lookup_logger):
                inv_idx.load_from_file(inv_index_file, logger=error_logger)
                pos_idx.load_from_file(pos_index_file, logger=error_logger)
                with open(vocab_dict_file, 'r', encoding='utf-8') as f:
                    vocab = json.load(f)
                for token, freq in vocab.items():
                    if isinstance(freq, int):
                        dict_set[token] = freq
                    else:
                        dict_set.setdefault(token, {}).update(freq)
                continue
            
            pattern = tokenizer.get_pattern()
            for i, word in enumerate(re.findall(pattern, data)):
                tokens = tokenizer.preprocess(word)
                token_length += len(tokens)
                for token in tokens:  
                    if token.lower() not in tokenizer.stop_words:
                        if tokenizer.has_number(token.lower()) and not tokenizer.is_number(token.lower()):
                            token = tokenizer.replace_numbers(token) 
                        stemmed_token = stemmer.stem(token.strip())

                        
                        dict_token = token.lower()
                        if not tokenizer.has_number(dict_token):
                            if not dict_token in local_dict:
                                local_dict[dict_token] = 1
                                dict_set[dict_token] = 1
                            else:
                                local_dict[dict_token] += 1
                                dict_set[dict_token] += 1
                        stemmed_tokens.append(stemmed_token)
                        
                        # Local For Loading Sved Indexes
                        local_inv_idx.add_to_index(doc_id=doc_id, token=stemmed_token)
                        local_pos_idx.add_to_index(doc_id=doc_id, token=stemmed_token, position=i)  #? Is it good to add positions wrt docs (not stemmed docs!)

                        # global indexes
                        inv_idx.add_to_index(doc_id=doc_id, token=stemmed_token)
                        pos_idx.add_to_index(doc_id=doc_id, token=stemmed_token, position=i)


            metadata.update(
                {
                    "tokens": token_length,
                    "unique_tokens": len(local_dict),
                    "stemmed_tokens": len(stemmed_tokens),
                    "inv_index_file": inv_index_file,
                    "pos_index_file": pos_index_file,
                    "vocab_file": vocab_dict_file
                }
            )

            log_message(json.dumps(metadata, indent=4), logger=metadata_logger)

            write_data(inv_index_file, local_inv_idx.index)
            write_data(pos_index_file, local_pos_idx.index)
            write_data(vocab_dict_file, local_dict)


    os.makedirs('docs', exist_ok=True)
    with open("./docs/inv-index.json", "w", encoding="utf-8") as f:
        json.dump(inv_idx.index, f, indent=4)
    with open("./docs/pos-index.json", "w", encoding="utf-8") as f:
        json.dump(pos_idx.index, f, indent=4)
    with open("./docs/dict-set.json", "w", encoding="utf-8") as f:
        json.dump(dict_set, f, indent=4)
    


# if __name__ == "__main__":
#     processor("./ResearchPapers/")
