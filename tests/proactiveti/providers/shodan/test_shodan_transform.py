"""proactiveti.providers.shodan.transform unit tests."""
from copy import deepcopy

import pytest

from proactiveti.providers.shodan.transform import transform_to_ecs, transform_to_observables, transform_to_observables


# Pytest fixture for Shodan results
@pytest.fixture
def shodan_fixture():
    """
    Returns a list of dictionaries representing Shodan data for testing purposes.

    Each dictionary contains the following keys:
    - ip_str: a string representing an IP address
    - port: an integer representing a port number
    - hostnames: a list of strings representing hostnames associated with the IP address
    """
    return [
        {
            'shodan': {
                'ip_str': '127.0.0.1',
                'port': 80,
                'hostnames': ['example.com']
            }
        }
    ]

def test_transform_to_ecs(shodan_fixture):
    """Test transform_to_ecs function."""
    transformed_results = transform_to_ecs(shodan_fixture)

    # Test if the transformed results have the expected structure
    for result in transformed_results:
        assert 'destination' in result
        assert 'shodan' in result

def test_transform_to_observables():
    """Test transform_to_observables function."""
    # Sample Shodan results
    shodan_results = [
        {'ip_str': '127.0.0.1'},
        {'ip_str': '192.168.1.1', 'hostnames': ['example.com', 'example.org']}
    ]

    observables = transform_to_observables(shodan_results, hostnames=True)

    # Test if the observables list is not empty
    assert observables


def test_transform_to_observables():
    """Test transform_to_observables function."""
    # Sample Shodan results
    shodan_results = [
        {'ip_str': '127.0.0.1'},
        {'ip_str': '192.168.1.1', 'hostnames': ['example.com', 'example.org']}
    ]

    observables = transform_to_observables(shodan_results, hostnames=True)

    # Test if the observables list is not empty
    assert observables

    assert '127.0.0.1' in observables
    assert 'example.com' in observables
    assert 'example.org' in observables
