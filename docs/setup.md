# Setup

Clone the repo

```shell
git clone git@github.com:brett-fitz/proactiveti.git
```

Install the proactiveti package and CLI

=== "General"

    Install proactiveti

    ```shell
    poetry install
    ```

=== "Select env python version"

    Set python environment

    ```shell
    poetry env use 3.11
    ```

    Install proactiveti

    ```shell
    poetry install
    ```

Run `proactiveti`

```shell
❯ poetry run proactiveti 
Usage: proactiveti [OPTIONS] COMMAND [ARGS]...

  Python CLI Core

Options:
  -v, --verbose  Verbose logging
  -h, --help     Show this message and exit.
```
