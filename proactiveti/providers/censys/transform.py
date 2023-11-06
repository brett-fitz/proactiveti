"""proactiveti.censys module: transform"""
from copy import deepcopy
import logging
from typing import Dict, List


__all__ = [
    "transform_to_ecs"
]

logger = logging.getLogger(__name__)


def transform_to_ecs(results: List[Dict]) -> List[Dict]:
    """Transform Censys results to ECS 

    Args:
        results: Results returned from Censys search.

    Returns:
        Transformed results in ECS format.
    """
    # Translate coordinates to geo_point format
    for result in results:
        if result.get('location', {}).get('coordinates'):
            result['location']['coordinates'] = {
                'lat': result['location']['coordinates']['latitude'],
                'lon': result['location']['coordinates']['longitude']
            }

    return [
        {
            'destination': {
                'address': result['ip'],
                'ip': result['ip'],
                'port': matched_service['port']
            },
            'censys': deepcopy(result)
        }
        for result in results
        for matched_service in result['matched_services']
    ]
