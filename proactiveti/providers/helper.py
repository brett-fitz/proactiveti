"""proactiveti.providers module: helper"""
import logging
from typing import Dict, List, Union

from proactiveti.providers import censys
from proactiveti.providers import shodan


__all__ = [
    "execute_search"
]

logger = logging.getLogger(__name__)


def execute_search(module: Dict, transform_format: str) -> Union[List[Dict], List[str]]:
    """Execute a search using specified providers in the module and transform results
    based on the write format.

    Args:
        module (Dict): A dictionary containing search module configurations,
            including providers and queries.
        transform_format (str): The desired format for writing results ('ecs' or 'observables').

    Returns:
        Union[List[Dict], List[str]]: A list of transformed results based on
            the specified write format.

    Example:
        Given a module configuration:
        ```
        module = {
            'providers': ['censys', 'shodan'],
            'censys': {
                'query': 'example_query',
                'reverse_dns': True,
                'tls_certificate': False
            },
            'shodan': {
                'query': 'example_query',
                'hostnames': True
            }
        }
        ```

        The function call `execute_search(module, transform_format='ecs')` would return a list
            of ECS-compliant results.

    Note:
        This function supports providers such as 'censys' and 'shodan'. 
        The write format can be 'ecs' for Elastic Common Schema or 'observables'.
    """
    transformed_results = []

    # Loop through providers in module
    for provider in module['providers']:
        if provider == 'censys':
            results = censys.search(
                query=module[provider]['query'],
            )
            if transform_format == 'ecs':
                transformed_results += censys.transform_to_ecs(
                    results=results,
                    reverse_dns=module[provider]['reverse_dns']
                )
            else:
                transformed_results += censys.transform_to_observables(
                    results=results,
                    reverse_dns=module[provider]['reverse_dns'],
                    tls_certificate=module[provider]['tls_certificate']
                )
        elif provider == 'shodan':
            results = shodan.search(
                query=module[provider]['query'],
            )
            if transform_format == 'ecs':
                transformed_results += shodan.transform_to_ecs(
                    results=results,
                    hostnames=module[provider]['hostnames']
                )
            else:
                transformed_results += shodan.transform_to_observables(
                    results=results,
                    hostnames=module[provider]['hostnames']
                )

    return transformed_results
