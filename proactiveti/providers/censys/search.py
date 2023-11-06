"""
proactiveti.providers.censys module: search
"""
from typing import Dict, List
import logging

from censys.search import CensysHosts


__all__ = [
    "search"
]

logger = logging.getLogger(__name__)


def _search(
    query: str,
    api_id: str = None,
    api_secret: str = None,
    **kwargs
) -> Dict:
    client = CensysHosts(api_id, api_secret)
    return [
        result
        for page in client.search(query=query, pages=-1, **kwargs)
        for result in page
    ]


def search(
    query: str,
    api_id: str,
    api_secret: str,
    reverse_dns: bool = False,
    tls_certificate: bool = False,
    full_log: bool = False
) -> List[str]:
    """
    Search Censys data for observables.

    Args:
        query: The search query.
        api_id: Your Censys API ID.
        api_secret: Your Censys API secret.
        reverse_dns: Allow Reverse DNS observables.
        tls_certificate: Allow observables to be extracted from TLS certificates.
        full_log: Append the full log to each result record.

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
        ] if not full_log else None
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
