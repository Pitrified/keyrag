"""Keyrag project configuration."""

from loguru import logger as lg

from keyrag.config.keyrag_paths import KeyragPaths
from keyrag.config.singleton import Singleton


class KeyragConfig(metaclass=Singleton):
    """Keyrag project configuration."""

    def __init__(self) -> None:
        lg.info(f"Loading Keyrag config")
        self.paths = KeyragPaths()

    def __str__(self) -> str:
        s = "KeyragConfig:"
        s += f"\n{self.paths}"
        return s

    def __repr__(self) -> str:
        return str(self)


def get_keyrag_config() -> KeyragConfig:
    """Get the keyrag config."""
    return KeyragConfig()


def get_keyrag_paths() -> KeyragPaths:
    """Get the keyrag paths."""
    return get_keyrag_config().paths
