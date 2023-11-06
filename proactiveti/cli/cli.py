"""proactiveti.cli module: cli"""
import asyncio
from functools import wraps
import logging
from pathlib import Path
from typing import List

import click
import coloredlogs
import yaml

from proactiveti.utils import validate_yaml


__all__ = [
    "cli"
]


@click.group()
@click.option("-v", "--verbose", is_flag=True, default=False, help="Verbose logging")
@click.help_option('-h', '--help')
def cli(verbose: bool):
    """Threat Analysis CLI"""
    # This is added as a header to the help output
    log_level = logging.DEBUG if verbose else logging.INFO
    coloredlogs.install(level=log_level)


def click_async(func):
    """A decorator to run Click commands asychronously"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        """Wrapper"""

        return asyncio.run(func(*args, **kwargs))

    return wrapper


@cli.command()
@click.argument("modules", type=click.STRING, nargs=-1, required=True)
@click.option("-F", "--format", type=click.Choice(['json', 'csv']), default='json', help="Output file format: default json")
def leads(
    modules: List[str],
    write_format: str
):
    """Execute lead modules and output observable files"""
    for module in modules:
        # load module
        module = yaml.safe_load(Path(module).read_text('utf-8'))

        # vaidate module with schema
        validate_yaml(input_file=Path(module), schema_file=Path())
        
        # for each configured provider execute search query
        
