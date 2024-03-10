import os
import re
import json
import logging
from src.tokenizer import Tokenizer
from src.porter_stemmer import PorterStemmer
from src.inverted_index import InvertedIndex
from src.positional_index import PositionalIndex
from src.utils import *
from typing import List, Dict, Tuple, Any

INDEX_FILES = "indexes"
VOCAB_FILES = "vocab"

class IndexProcessor:
    def __init__(self, data_dir: str, exclude_files: List[str] = ["Stopword-List.txt"]) -> None:
        """
        Initializes an IndexProcessor instance.

        Args:
            data_dir (str): Data directory path.
            exclude_files (List[str]): List of files to exclude during processing. Default is ["Stopword-List.txt"].
        """
        self.data_dir = data_dir
        self.exclude_files = exclude_files
        self.inv_idx = InvertedIndex()
        self.pos_idx = PositionalIndex()
        self.local_inv_idx = None
        self.local_pos_idx = None
        self.dict_set: Dict[str, int] = {}
        self.local_dict: Dict[str, int] = {}
        self.tokenizer = Tokenizer()
        self.stemmer = PorterStemmer()
        
    @timing_decorator
    def process_data(self) -> Tuple[InvertedIndex, PositionalIndex, Dict[str, int]]:
        """
        Reads data from the directory and creates positional and inverted indexes.
        """
        files = list_files(self.data_dir, self.exclude_files)
        index_dir = "./src/" + INDEX_FILES
        vocab_file = "./src/" + VOCAB_FILES
        os.makedirs(index_dir, exist_ok=True)
        os.makedirs(vocab_file, exist_ok=True)
        metadata_logger = get_logger("metadata", see_time=False, console_log = False, level = logging.INFO)
        lookup_logger = get_logger("lookup", see_time = True, console_log = False, level = logging.INFO)
        error_logger = get_logger("processor_error",see_time = True,console_log = CONSOLE_LOGS,level = logging.ERROR,)
        logged_metadata = read_metadata("metadata")
        file_iter = 1

        for file in files:
            self.local_inv_idx = InvertedIndex()
            self.local_pos_idx = PositionalIndex()
            self.local_dict = {}
            if file.endswith(".txt"):
                data = read_data(file)
                doc_id = re.findall(r'[^\\/]*$', file)
                doc_id = doc_id[0].split(".")[0]
                doc_id = str(file_iter) + "_" + doc_id
                file_iter += 1
                self.process_file(
                    data,
                    doc_id,
                    index_dir,
                    vocab_file,
                    logged_metadata,
                    metadata_logger,
                    lookup_logger,
                    error_logger,
                )

        self.save_indexes()
        return self.inv_idx, self.pos_idx, self.dict_set

    def process_file(
        self,
        data: str,
        doc_id: str,
        index_dir: str,
        vocab_file: str,
        logged_metadata: Dict[str, str],
        metadata_logger,
        lookup_logger,
        error_logger,
    ) -> None:
        """
        Processes an individual file, updating indexes and metadata.

        Args:
            data (str): Content of the file.
            doc_id (str): Document ID.
            index_dir (str): Directory to save index files.
            vocab_file (str): Directory to save vocabulary files.
            logged_metadata (Dict[str, str]): Previously logged metadata.
            metadata_logger: Logger for metadata.
            lookup_logger: Logger for metadata lookup.
            error_logger: Logger for errors.
        """
        inv_index_file = os.path.join(index_dir, f"{doc_id}_ivnIdx.json")
        pos_index_file = os.path.join(index_dir, f"{doc_id}_posIdx.json")
        vocab_dict_file = os.path.join(vocab_file, f"{doc_id}_vocab.json")

        metadata = {"doc_id": doc_id}
        if metadata_lookup(metadata, logged_metadata, logger=lookup_logger):
            self.load_indexes(inv_index_file, pos_index_file, vocab_dict_file, error_logger)
            return

        tokens_length = 0
        stemmed_token_length = 0
        pattern = self.tokenizer.get_pattern()
        for i, word in enumerate(re.findall(pattern, data)):
            tokens = self.tokenizer.preprocess(word)
            tokens_length += len(tokens) if tokens is not [] else 0
            for token in tokens:
                if token.lower() not in self.tokenizer.stop_words:
                    if self.tokenizer.has_number(token.lower()) and not self.tokenizer.is_number(token.lower()):
                        token = self.tokenizer.replace_numbers(token)
                    stemmed_token = self.stemmer.stem(token.strip())
                    stemmed_token_length += 1
                    dict_token = token.lower()
                    self.update_dict(doc_id, dict_token)
                    self.update_indexes(doc_id, stemmed_token, i)

        metadata.update(
                {
                    "tokens": tokens_length,
                    "unique_tokens": len(self.local_dict),
                    "stemmed_tokens": stemmed_token_length,
                    "inv_index_file": inv_index_file,
                    "pos_index_file": pos_index_file,
                    "vocab_file": vocab_dict_file
                }
            )

        log_message(json.dumps(metadata, indent=4), logger=metadata_logger)

        write_data(inv_index_file, self.inv_idx.index)
        write_data(pos_index_file, self.pos_idx.index)
        write_data(vocab_dict_file, self.dict_set)

    def update_dict(self, doc_id: str, dict_token: str) -> None:
        """
        Updates the local dictionary.

        Args:
            doc_id (str): Document ID.
            dict_token (str): Token in the original form.
        """
        if not self.tokenizer.has_number(dict_token):
            if dict_token not in self.local_dict:
                self.local_dict[dict_token] = 1
                self.dict_set[dict_token] = 1
            else:
                self.local_dict[dict_token] += 1
                self.dict_set[dict_token] += 1

    def update_indexes(self, doc_id: str, stemmed_token: str, position: int) -> None:
        """
        Updates  indexes..

        Args:
            doc_id (str): Document ID.
            stemmed_token (str): Stemmed token.
            position (int): Token position in the document.
        """
        self.local_inv_idx.add_to_index(doc_id=doc_id, token=stemmed_token)
        self.local_pos_idx.add_to_index(
            doc_id=doc_id, token=stemmed_token, position=position
        )
        self.inv_idx.add_to_index(doc_id=doc_id, token=stemmed_token)
        self.pos_idx.add_to_index(doc_id=doc_id, token=stemmed_token, position=position)

    @timing_decorator
    def load_indexes(self, inv_index_file: str, pos_index_file: str, vocab_dict_file: str, error_logger) -> None:
        """
        Loads indexes from saved files.

        Args:
            inv_index_file (str): Inverted index file path.
            pos_index_file (str): Positional index file path.
            vocab_dict_file (str): Vocabulary dictionary file path.
            error_logger: Logger for errors.
        """
        self.inv_idx.load_from_file(inv_index_file, logger=error_logger)
        self.pos_idx.load_from_file(pos_index_file, logger=error_logger)
        with open(vocab_dict_file, "r", encoding="utf-8") as f:
            vocab = json.load(f)
        for token, freq in vocab.items():
            if isinstance(freq, int):
                self.dict_set[token] = freq
            else:
                self.dict_set.setdefault(token, {}).update(freq)

    @timing_decorator
    def save_indexes(self) -> None:
        """
        Saves the global indexes to files.
        """
        os.makedirs("docs", exist_ok=True)
        with open("./docs/inv-index.json", "w", encoding="utf-8") as f:
            json.dump(self.inv_idx.index, f, indent=4)
        with open("./docs/pos-index.json", "w", encoding="utf-8") as f:
            json.dump(self.pos_idx.index, f, indent=4)
        with open("./docs/dict-set.json", "w", encoding="utf-8") as f:
            json.dump(self.dict_set, f, indent=4)



