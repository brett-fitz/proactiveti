"""
proactiveti.auth.secrets_manager module: secrets_manager
"""
from __future__ import annotations
import base64
from functools import lru_cache
import json
import logging
from typing import TYPE_CHECKING, Dict, List, Union

from boto3 import Session

from proactiveti.auth.secrets_manager.constants import (
    CENSYS_SECRET_NAME,
    SECRETS_PROFILE,
    SECRETS_REGION,
    SHODAN_SECRET_NAME
)

if TYPE_CHECKING:
    from mypy_boto3_secretsmanager.client import SecretsManagerClient


__all__ = [
    "get_secret",
    "get_censys_secret",
    "get_shodan_secret",
]

logger = logging.getLogger(__name__)

# Setup AWS session
AWS_SESSION = Session(profile_name=SECRETS_PROFILE)

# Setup AWS Secrets Manager client
client: SecretsManagerClient = AWS_SESSION.client(
    "secretsmanager",
    region_name=SECRETS_REGION
)


def get_secret(secret_name: str) -> Union[str, bytes, List, Dict]:
    """Retrieve a secret from the AWS Secrets Manager using its name.

    Args:
        secret_name (str): The name or ARN of the secret to retrieve.

    Returns:
        Union[str, bytes, List, Dict]: The secret value, decoded based on its type.

    Example:
        Given a secret named 'example_secret' with the following JSON content:
        ```
        {"username": "admin", "password": "secretpassword"}
        ```

        The function call `get_secret('example_secret')` would return:
        ```
        {'username': 'admin', 'password': 'secretpassword'}
        ```

    Note:
        This function can handle both JSON string and binary secrets.
    """
    resp = client.get_secret_value(SecretId=secret_name)

    if 'SecretString' in resp:
        secret = json.loads(resp['SecretString'])
    else:
        secret = base64.b64decode(resp['SecretBinary'])

    return secret


@lru_cache(maxsize=None)
def get_censys_secret() -> Dict[str, str]:
    """Retrieve the Censys API key from the Secrets Manager.

    Returns:
        Dict[str, str]: A dictionary containing the Censys API key.

    Example:
        The function call `get_censys_secret()` would return:
        ```
        {'api_id': 'your_censys_api_id', 'api_secret': 'your_censys_api_secret'}
        ```
    """
    return get_secret(CENSYS_SECRET_NAME)


@lru_cache(maxsize=None)
def get_shodan_secret() -> Dict[str, str]:
    """Retrieve the Shodan API key from the Secrets Manager.

    Returns:
        Dict[str, str]: A dictionary containing the Shodan API key.

    Example:
        The function call `get_shodan_secret()` would return:
        ```
        {'api_key': 'your_shodan_api_key'}
        ```
    """
    return get_secret(SHODAN_SECRET_NAME)
