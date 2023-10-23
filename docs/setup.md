# Setup

Clone the repo

```shell
git clone git@github.com:brett-fitz/python-cli.git
```

Install the pycli package and CLI

=== "General"

    Install pycli

    ```shell
    poetry install
    ```

=== "Select env python version"

    Set python environment

    ```shell
    poetry env use 3.11
    ```

    Install pycli

    ```shell
    poetry install
    ```

Run `pycli`

```shell
❯ poetry run pycli 
Usage: pycli [OPTIONS] COMMAND [ARGS]...

  Python CLI Core

Options:
  -v, --verbose  Verbose logging
  -h, --help     Show this message and exit.
```
