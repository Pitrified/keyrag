"""Embeddings config for OpenAI embeddings."""

from enum import Enum

from langchain_core.embeddings.embeddings import Embeddings
from langchain_openai import OpenAIEmbeddings
from pydantic import Field, SecretStr

from keyrag.embed.embeddings_config import EmbeddingsConfig
from keyrag.utils.langchain_ import get_secret_from_env


class OpenAIEmbeddingModelName(Enum):
    text_embedding_3_small = "text-embedding-3-small"


class OpenAIEmbeddingsConfig(EmbeddingsConfig):
    """Config for OpenAI embeddings.

    OpenAIEmbeddings in langchain_openai/embeddings/base.py
    already has a truckload of parameters.
    That we could all set.
    """

    model: OpenAIEmbeddingModelName = Field(
        ..., description="The name of the OpenAI model to use."
    )
    api_key: SecretStr = Field(..., description="OpenAI API key.")

    def to_embeddings(self) -> Embeddings:
        ef = OpenAIEmbeddings(**self.model_dump())
        return ef


OPENAI_EMBEDDINGS_CONFIG_DEFAULT = OpenAIEmbeddingsConfig(
    model=OpenAIEmbeddingModelName.text_embedding_3_small,
    api_key=get_secret_from_env("OPENAI_API_KEY"),
)
