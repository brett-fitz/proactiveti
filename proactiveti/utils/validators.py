"""proactiveti.utils module: validators"""
import logging

import validators
import yamale


__all__ = [
    "validate_yaml"
]

logger = logging.getLogger(__name__)


def is_domain_or_ip(observable: str) -> str:
    """
    Validate whether the given observable is a domain or an IP address.

    Args:
        observable (str): The observable to be validated.

    Returns:
        str: "domain-name" if the observable is a domain, "ipv4-addr" if the observable is an IPv4
            address, "ipv6-addr" if the observable is an IPv6 address, or "unknown" if the
            observable is neither a domain nor an IP address.
    """
    if validators.ipv4(observable):
        return "ipv4-addr"
    if validators.ipv6(observable):
        return "ipv6-addr"
    if validators.domain(observable):
        return "domain-name"
    return "unknown"


def validate_yaml(input_file: str, schema_file: str) -> None:
    """
    Validate whether the input YAML file conforms to the specified schema.

    Args:
        input_file (str): Path to the input YAML file.
        schema_file (str): Path to the YAML schema file.

    Raises:
        yamale.yamale_error.YamaleError: If validation fails.

    Returns:
        None
    """
    # Load schema
    schema = yamale.make_schema(schema_file)

    # Load data
    data = yamale.make_data(input_file)

    # Validate
    yamale.validate(schema, data)
