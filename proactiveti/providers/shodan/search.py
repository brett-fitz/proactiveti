"""
proactiveti.providers.shodan module: search
"""
import logging
from typing import List

from shodan import Shodan


__all__ = [
    "search"
]

logger = logging.getLogger(__name__)


def search(
    query: str,
    api_key: str,
    num_results: int = None,
    hostnames: bool = False
) -> List[str] | None:
    """
    Performs a shodan search and returns a list of observables.

    Args:
        query: Search query.
        api_key: Shodan api key.
        num_results: Limit the number of results returned.
        hostnames: Include hostnames for the ip log in the returned list of observables.

    Returns:
        A list of results or None.
    """
    api = Shodan(api_key)

    logger.info(f'Executing query: {query}')
    result_count = api.count(query)['total']
    if result_count == 0:
        logger.warning(f'query: {query} returned 0 results')
        return None

    logger.info(f'query: {query} returned {result_count} results')
    results = []
    for index, result in enumerate(api.search_cursor(query)):
        # ip address
        if num_results and index >= num_results:
            break
        results.append(result['ip_str'])

        # hostnames
        if hostnames and result.get('hostnames') and result['hostnames']:
            for host in result['hostnames']:
                results.append(host)

    results = list(set(results))
    logger.info(f'query: {query} produced {len(results)} observables')
    return results
