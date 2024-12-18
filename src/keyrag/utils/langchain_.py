"""Utils for the langchain package."""

from langchain_core.utils.utils import secret_from_env
from pydantic import SecretStr


def get_secret_from_env(env_var: str) -> SecretStr:
    """Get a secret from an environment variable."""
    return secret_from_env(env_var)()
