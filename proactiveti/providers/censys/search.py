"""proactiveti.providers.censys module: search"""

from typing import List
import logging

from censys.search import CensysHosts


__all__ = [
    "search"
]

logger = logging.getLogger(__name__)

def search(
    query: str,
    api_id: str,
    api_secret: str,
    reverse_dns: bool = False,
    tls_certificate: bool = False
) -> List[str]:
    """
    Search Censys data for observables.

    Args:
        query (str): The search query.
        api_id (str): Your Censys API ID.
        api_secret (str): Your Censys API secret.
        reverse_dns (bool, optional): Allow Reverse DNS observables. Default is False.
        tls_certificate (bool, optional): Allow TLS observables to be extracted from TLS certificates. Default is False.

    Returns:
        List[str]: List of unique indicators found in the search results.
    """
    client = CensysHosts(api_id, api_secret)

    indicators = set()

    for page in client.search(
        query=query,
        pages=-1,
        fields=['dns.reverse_dns.names', 'services.tls.certificates.leaf_data.names']
    ):
        for result in page:
            if result.get('ip'):
                indicators.add(result['ip'])
            if reverse_dns and result.get('dns'):
                indicators |= set(result['dns']['reverse_dns']['names'])
            if tls_certificate and result.get('services'):
                for service in result['services']:
                    if 'tls' in service and 'certificates' in service['tls'] and 'leaf_data' in service['tls']['certificates']:
                        indicators |= set(service['tls']['certificates']['leaf_data']['names'])
    return list(indicators)
