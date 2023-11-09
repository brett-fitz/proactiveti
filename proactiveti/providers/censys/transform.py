"""
proactiveti.censys module: transform

TODO
- Extract tls_certificate observables - need to warn user about FPs or manage
via misp-warninglists, etc

- Currently we only support extracting ovservables from the 'matched_services'
which requires a paid license. We should also support extracting observables from
the 'services' field which is available to free users.

"""
from copy import deepcopy
import logging
from typing import Dict, List, Set


__all__ = [
    "transform_to_ecs",
    "transform_to_observables"
]

logger = logging.getLogger(__name__)


def transform_to_ecs(
    results: List[Dict],
    reverse_dns: bool = False
) -> List[Dict]:
    """Transforms Censys search results into Elastic Common Schema (ECS) format.

    Args:
        results (List[Dict]): A list of dictionaries containing Censys search results.
        reverse_dns (bool, optional): Whether to include hostnames via reverse DNS in
            the transformed ECS results. Defaults to False.

    Returns:
        List[Dict]: A list of dictionaries representing ECS-compliant results.

    Example:
        Given a Censys result:
        {
            'ip': '127.0.0.1',
            'location': {
                'coordinates': {
                    'latitude': 37.7749,
                    'longitude': -122.4194
                }
            },
            'matched_services': [
                {
                    'port': 80
                }
            ],
            'dns': {
                'reverse_dns': {
                    'names': ['example.com']
                }
            }
        }

        The transformed ECS result may look like:
        {
            'destination': {
                'address': '127.0.0.1',
                'ip': '127.0.0.1',
                'port': 80
            },
            'censys': {...},
            'location': {
                'coordinates': {
                    'lat': 37.7749,
                    'lon': -122.4194
                }
            }
        }
        or
        {
            'destination': {
                'address': 'example.com',
                'domain': 'example.com',
                'ip': '127.0.0.1',
                'port': 80
            },
            'censys': {...},
            'location': {
                'coordinates': {
                    'lat': 37.7749,
                    'lon': -122.4194
                }
            }
        }

    Note:
        The 'location' coordinates are translated to the geo_point format required by ECS.
    """
    # Translate coordinates to geo_point format
    for result in results:
        if result.get('location', {}).get('coordinates'):
            result['location']['coordinates'] = {
                'lat': result['location']['coordinates']['latitude'],
                'lon': result['location']['coordinates']['longitude']
            }

    transformed_results: List[Dict] = []

    for result in results:
        for matched_service in result['matched_services']:
            # ip address
            transformed_results.append(
                {
                    'destination': {
                        'address': result['ip'],
                        'ip': result['ip'],
                        'port': matched_service['port']
                    },
                    'censys': deepcopy(result)
                }
            )

            # hostnames via reverse_dns
            if reverse_dns and result.get('dns'):
                for observable in result['dns']['reverse_dns']['names']:
                    transformed_results.append(
                        {
                        'destination': {
                            'address': observable,
                            'domain': observable,
                            'ip': result['ip'],
                            'port': matched_service['port']
                        },
                        'censys': deepcopy(result)
                    }
                )

    return transformed_results


def transform_to_observables(
    results: List[Dict],
    reverse_dns: bool = False,
    tls_certificate: bool = False,
) -> List[str]:
    """Transforms Censys search results into a list of simple observables.

    Args:
        results (List[Dict]): A list of dictionaries containing Censys search results.
        reverse_dns (bool, optional): Whether to include DNS observables via reverse DNS
            in the transformed list. Defaults to False.
        tls_certificate (bool, optional): Whether to include TLS observables in the
            transformed list. Defaults to False.

    Returns:
        List[str]: A list of unique observables extracted from the input Censys search results.

    Example:
        Given a Censys result:
        {
            'ip': '127.0.0.1',
            'dns': {
                'reverse_dns': {
                    'names': ['example.com']
                }
            },
            'services': [
                {
                    'tls': {
                        'certificates': {
                            'leaf_data': {
                                'names': ['example.com']
                            }
                        }
                    }
                }
            ]
        }

        The transformed list of observables may look like:
        ['127.0.0.1', 'example.com']

    Note:
        The observables include IP addresses, DNS names via reverse DNS, and
        TLS certificate names if enabled.
    """
    observables: Set[str] = set()

    for result in results:
        # IP observable
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
