"""Embeddings config base class."""

from abc import ABC, abstractmethod

from langchain_core.embeddings.embeddings import Embeddings
from pydantic import BaseModel


class EmbeddingsConfig(BaseModel, ABC):

    @abstractmethod
    def to_embeddings(self) -> Embeddings:
        """Convert the config to an Embeddings object."""
