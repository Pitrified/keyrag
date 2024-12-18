"""Test the keyrag paths."""

import pytest

from keyrag.config.keyrag_config import get_keyrag_paths


def test_keyrag_paths() -> None:
    """Test the keyrag paths."""
    keyrag_paths = get_keyrag_paths()
    assert keyrag_paths.src_fol.name == "keyrag"
    assert keyrag_paths.root_fol.name == "keyrag"
    assert keyrag_paths.data_fol.name == "data"
