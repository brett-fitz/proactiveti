

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
    """Reads multiple YAML files asynchronously and returns a list of parsed contents as dictionaries.

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