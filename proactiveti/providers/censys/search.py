"""
proactiveti.providers.censys module: search
"""
from typing import Dict, List
import logging
import os

from censys.search import CensysHosts

from proactiveti.auth import AUTH_SCHEMA
from proactiveti.auth.secrets_manager import get_censys_secret


__all__ = [
    "search"
]

logger = logging.getLogger(__name__)


def search(
    query: str,
    api_id: str = None,
    api_secret: str = None,
    **kwargs
) -> List[Dict]:
    """Performs a Censys search query and returns the results.

    Args:
        query (str): The Censys search query to be executed.
        api_id (str, optional): Censys API ID for authentication. Defaults to None.
        api_secret (str, optional): Censys API secret for authentication. Defaults to None.
        **kwargs: Additional keyword arguments to be passed to the Censys search API.

    Returns:
        List[Dict]: A list of dictionaries representing the search results.

    Example:
        Given a Censys search query:
        ```
        search("protocol:https")
        ```
        The function returns a list of dictionaries containing information about hosts with
        the HTTPS protocol.

    Note:
        Censys API credentials (api_id and api_secret) are required for authentication.

    See Also:
        Censys API Documentation: https://search.censys.io/api
    """
    if not api_id or not api_secret:
        if AUTH_SCHEMA.get('censys', {}).get('type') == 'env':
            api_id = os.getenv(AUTH_SCHEMA.get('censys', {}).get('api_id'))
            api_secret = os.getenv(AUTH_SCHEMA.get('censys', {}).get('api_secret'))
        elif AUTH_SCHEMA.get('censys', {}).get('type') == 'secrets_manager':
            censys_secret = get_censys_secret()
            api_id = censys_secret.get('api_id')
            api_secret = censys_secret.get('api_secret')
        else:
            logger.error(
                "Censys API credentials (api_id and api_secret) are required for authentication."
            )
            return None
    client = CensysHosts(api_id, api_secret)

    # Use list comprehension to flatten the results from multiple pages
    return [
        result
        for page in client.search(query=query, pages=-1, **kwargs)
        for result in page
    ]
