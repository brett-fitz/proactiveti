"""
proactiveti.auth.secrets_manager module: constants
"""
from pathlib import Path


__all__ = [
    "SECRETS_PROFILE",
    "SECRETS_REGION",
]

AUTH_SCHEMA = Path(__file__).parent.parent.parent / "auth.yaml"

CENSYS_SECRET_NAME = AUTH_SCHEMA.get('censys', {}).get('secret_name')
SHODAN_SECRET_NAME = AUTH_SCHEMA.get('shodan', {}).get('secret_name')

SECRETS_PROFILE = AUTH_SCHEMA.get('aws', {}).get('profile')
SECRETS_REGION = AUTH_SCHEMA.get('aws', {}).get('region')
