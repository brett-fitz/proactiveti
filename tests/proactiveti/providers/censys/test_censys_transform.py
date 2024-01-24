"""proactiveti.providers.censys.transform unit tests."""
import pytest

from proactiveti.providers.censys.transform import transform_to_ecs, transform_to_observables


@pytest.fixture
def results():
    """Returns a list of results."""
    return [
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
                                'names': ['tls-example.com']
                            }
                        }
                    }
                }
            ]
        }
    ]


def test_transform_to_ecs_without_reverse_dns(results):
    """Test transform_to_ecs without reverse DNS."""
    expected = [
        {
            'destination': {
                'address': '127.0.0.1',
                'ip': '127.0.0.1',
                'port': 80
            },
            'censys': results[0]
        }
    ]
    actual = transform_to_ecs(results)
    assert actual == expected


def test_transform_to_ecs_with_reverse_dns(results):
    """Test transform_to_ecs with reverse DNS."""
    expected = [
        {
            'destination': {
                'address': '127.0.0.1',
                'ip': '127.0.0.1',
                'port': 80
            },
            'censys': results[0]
        },
        {
            'destination': {
                'address': 'example.com',
                'domain': 'example.com',
                'ip': '127.0.0.1',
                'port': 80
            },
            'censys': results[0]
        }
    ]
    actual = transform_to_ecs(results, reverse_dns=True)
    assert actual == expected


def test_transform_to_observables_ip_only(results):
    """Test transform_to_observables with only IP."""
    expected = ['127.0.0.1']
    actual = transform_to_observables(results)
    assert set(actual) == set(expected)

def test_transform_to_observables_with_reverse_dns(results):
    """Test transform_to_observables with reverse DNS."""
    expected = ['127.0.0.1', 'example.com']
    actual = transform_to_observables(results, reverse_dns=True)
    assert set(actual) == set(expected)

def test_transform_to_observables_with_tls_certificate(results):
    """Test transform_to_observables with TLS certificate."""
    expected = ['127.0.0.1', 'tls-example.com']
    actual = transform_to_observables(results, tls_certificate=True)
    assert set(actual) == set(expected)

def test_transform_to_observables_with_reverse_dns_and_tls_certificate(results):
    """Test transform_to_observables with reverse DNS and TLS certificate."""
    expected = ['127.0.0.1', 'example.com', 'tls-example.com']
    actual = transform_to_observables(results, reverse_dns=True, tls_certificate=True)
    assert set(actual) == set(expected)
