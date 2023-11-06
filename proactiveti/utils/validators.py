"""proactiveti.utils module: validators"""
import logging

import yamale


__all__ = [
    "validate_yaml"
]

logger = logging.getLogger(__name__)


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
