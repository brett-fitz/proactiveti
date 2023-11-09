"""
proactiveti.providers.shodan module: search
"""
import logging
from typing import Dict, List

from shodan import APIError, Shodan


__all__ = [
    "search"
]

logger = logging.getLogger(__name__)


def search(
    query: str,
    api_key: str,
    limit: int = None
) -> List[Dict] | None:
    """
    Performs a shodan search and returns a list of results.

    Args:
        query (str): Search query.
        api_key (str): Shodan api key.
        limit (int, optional): Limit the number of results processed. Defaults to None.

    Returns:
        A list of results or None.
    """
    client = Shodan(api_key)

    # first get result count
    try:
        result_count = client.count(query)['total']
    except APIError as error:
        # soft failure here as we won't re-raise
        logger.error(error)
        return None

    if not result_count:
        logger.warning(f'{query} produced no results')
        return None

    # enumerate results
    results: List[Dict] = []
    for index, result in enumerate(client.search_cursor(query)):
        if limit and index >= limit:
            break
        results.append(result)

    return results
