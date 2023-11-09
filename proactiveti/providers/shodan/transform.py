"""proactiveti.shodan module: transform"""
from copy import deepcopy
import logging
from typing import Dict, List


__all__ = [
    "transform_to_ecs",
    "transform_to_observables"
]

logger = logging.getLogger(__name__)


def transform_to_ecs(
    results: List[Dict],
    hostnames: bool = False
) -> List[Dict]:
    """Transforms Shodan search query results into valid Elastic Common Schema (ECS) results.

    Args:
        results (List[Dict]): A list of dictionaries containing Shodan search query results.
        hostnames (bool, optional): Whether to include hostnames in the transformed ECS results. Defaults to False.

    Returns:
        List[Dict]: A list of dictionaries representing ECS-compliant results.

    Example:
        Given a Shodan result:
        {
            'shodan': {
                'ip_str': '127.0.0.1',
                'port': 80,
                'hostnames': ['example.com']
            }
        }

        The transformed ECS result may look like:
        {
            'destination': {
                'address': '127.0.0.1',
                'ip': '127.0.0.1',
                'port': 80
            }
        }
        or
        {
            'shodan': {
                'ip_str': '127.0.0.1',
                'port': 80,
                'hostnames': ['example.com']
            },
            'destination': {
                'address': 'example.com',
                'domain': 'example.com',
                'port': 80
            }
        }
    """
    dedup_results = {}

    for result in results:
        # ip address
        result = {
            "destination": {
                'address': result['shodan']['ip_str'],
                'ip': result['shodan']['ip_str'],
                'port': result['shodan']['port']
            }
        }

        if not (
            f'{result["destination"]["address"]}:{result["destination"]["port"]}'
            in dedup_results
        ):
            dedup_results[
                f'{result["destination"]["address"]}:{result["destination"]["port"]}'
            ] = result

        # hostnames
        if hostnames and result['shodan'].get('hostnames'):
            for host in result['shodan']['hostnames']:
                if not f"{host}:{result['shodan']['port']}" in dedup_results:
                    tmp = {
                        'shodan': deepcopy(result['shodan']),
                        'destination': {
                            'address': host,
                            'domain': host,
                            'port': result['shodan']['port']
                        }
                    }
                    dedup_results[f"{host}:{result['shodan']['port']}"] = tmp

    return [value for _key, value in dedup_results.items()]


def transform_to_observables(
    results: List[Dict],
    hostnames: bool = False
) -> List[str]:
    """Transforms a list of shodan results into a flat list of observables.

    Args:
        results (List[Dict]): A list of shodan results.
        hostnames (bool, optional): Whether to include hostnames as observables. Defaults to False.

    Returns:
        List[str]: A list of unique observables extracted from the input data.
    """
    observables = set()
    for result in results:
        # ip address
        observables.add(result['ip_str'])

        # hostnames
        if hostnames and result.get('hostnames') and result['hostnames']:
            for host in result['hostnames']:
                observables.add(host)

    results = list(set(results))
    logger.info(f'produced {len(results)} observables')
    return list(observables)
