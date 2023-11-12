"""
proactiveti.providers.shodan module: search
"""
import logging
from typing import Dict, List

from shodan import APIError, Shodan

from proactiveti.auth import AUTH_SCHEMA
from proactiveti.auth.secrets_manager import get_shodan_secret


__all__ = [
    "search"
]

logger = logging.getLogger(__name__)


def search(
    query: str,
    api_key: str = None,
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
    if not api_key:
        if AUTH_SCHEMA.get('shodan', {}).get('type') == 'env':
            api_key = os.getenv(AUTH_SCHEMA.get('shodan', {}).get('api_key'))
        elif AUTH_SCHEMA.get('shodan', {}).get('type') == 'secrets_manager':
            shodan_secret = get_shodan_secret()
            api_key = shodan_secret.get('api_key')
        else:
            logger.error('Shodan API key is required')
            return None
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
