"""pycli.cli module: cli"""
import asyncio
from functools import wraps
import logging

import click
import coloredlogs


__all__ = [
    "cli"
]


@click.group()
@click.option("-v", "--verbose", is_flag=True, default=False, help="Verbose logging")
@click.help_option('-h', '--help')
def cli(verbose: bool):
    """Python CLI Core"""           # This is added as a header to the help output
    log_level = logging.DEBUG if verbose else logging.INFO
    # Configure the module logger
    # module_name = __name__.split(".", maxsplit=1)[0]
    # module_log = logging.getLogger(module_name)
    # module_log.propagate = False

    # coloredlogs.install(logger=module_log, level=log_level, reconfigure=False)
    coloredlogs.install(level=log_level)  # root logger


def click_async(func):
    """A decorator to run Click commands asychronously"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        """Wrapper"""

        return asyncio.run(func(*args, **kwargs))

    return wrapper
