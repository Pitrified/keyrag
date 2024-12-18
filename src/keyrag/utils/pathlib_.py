"""Utils for pathlib module."""

from pathlib import Path


def check_create_fol(fol: Path) -> None:
    """Check if the folder exists, if not create it."""
    if not fol.exists():
        fol.mkdir(parents=True)
