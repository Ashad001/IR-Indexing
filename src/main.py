import os
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
    
    files: List[str] = os.listdir(data_dir)
    
    for file in files:
        if file.endswith('.txt'):
            data = read_data(os.path.join(data_dir, file))
            print(data)
            
if __name__=="__main__":
    main("../data/toy/")
    