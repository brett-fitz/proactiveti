"""
proactiveti.utils module: files
"""
import os
from typing import Dict, List

import aiofiles
import yaml


def get_files(path: str, search: str = None) -> List[str]:
    """Get a list of files in a directory and its subdirectories, optionally
    filtered by a search term.

    Args:
        path (str): The path to the directory to search for files.
        search (str, optional): If provided, only include files containing this search
            term in their names. Defaults to None.

    Returns:
        List[str]: A list of file paths matching the search criteria.

    Example:
        Given a directory structure:
        ```
        /root
            ├── dir1
            │   ├── file1.txt
            │   └── schema.yml
            ├── dir2
            │   ├── file2.txt
            │   └── file3.txt
            └── schema.yml
        ```

        The function call `get_files("/root", search="file")` would return:
        ```
        [
            '/root/dir1/file1.txt',
            '/root/dir2/file2.txt',
            '/root/dir2/file3.txt'
        ]
        ```
    """
    all_files = []

    for root, _dirs, files in os.walk(path):
        for file in files:
            # Skip files named 'schema.yml'
            if file == 'schema.yml':
                continue

            # Check if a search term is provided
            if not search:
                all_files.append(os.path.join(root, file))
            else:
                # Include files containing the search term in their names
                if search in file:
                    all_files.append(os.path.join(root, file))

    return all_files


async def read_yaml(file: str) -> Dict:
    """Reads a YAML file asynchronously and returns the parsed content as a dictionary.

    Args:
        file (str): The path to the YAML file to be read.

    Returns:
        Dict: A dictionary containing the parsed content of the YAML file.

    Example:
        Given a YAML file "example.yaml" with the following content:
        ```
        key1: value1
        key2:
          - item1
          - item2
        ```

        The function call `await read_yaml("example.yaml")` would return:
        ```
        {'key1': 'value1', 'key2': ['item1', 'item2']}
        ```
    """
    async with aiofiles.open(file, mode='r') as yaml_file:
        return yaml.safe_load(await yaml_file.read())


async def read_yaml_files(files: List[str]) -> List[Dict]:
    """Reads multiple YAML files asynchronously and returns a list of
    parsed contents as dictionaries.

    Args:
        files (List[str]): A list of paths to the YAML files to be read.

    Returns:
        List[Dict]: A list of dictionaries containing the parsed contents of the YAML files.

    Example:
        Given a list of YAML files ["file1.yaml", "file2.yaml"] with the following content:
        file1.yaml:
        ```
        key1: value1
        ```

        file2.yaml:
        ```
        key2: value2
        ```

        The function call `await read_yaml_files(["file1.yaml", "file2.yaml"])` would return:
        ```
        [
            {'key1': 'value1'},
            {'key2': 'value2'}
        ]
        ```
    """
    return [await read_yaml(file) for file in files]
