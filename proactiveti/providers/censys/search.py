"""
proactiveti.providers.censys module: search
"""
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
        reverse_dns (bool, optional): Allow Reverse DNS observables.
        tls_certificate (bool, optional): Allow observables to be extracted from TLS certificates.

    Returns:
        List[str]: List of unique observables found in the search results.
    """
    client = CensysHosts(api_id, api_secret)

    observables = set()

    for page in client.search(
        query=query,
        pages=-1,
        fields=[
            'dns.reverse_dns.names',
            'services.tls.certificates.leaf_data.names'
        ]
    ):
        for result in page:
            # IP observable
            if result.get('ip'):
                observables.add(result['ip'])
            # DNS observables
            if reverse_dns and result.get('dns'):
                observables |= set(result['dns']['reverse_dns']['names'])
            # TLS observables
            if tls_certificate and result.get('services'):
                for service in result['services']:
                    if service.get('tls', {}).get('certificates', {}).get('leaf_data'):
                        observables |= set(service['tls']['certificates']['leaf_data']['names'])
    
    return list(observables)
