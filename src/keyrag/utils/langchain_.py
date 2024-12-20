"""Utils for the langchain package."""

from langchain_core.documents import Document
from langchain_core.utils.utils import secret_from_env
from pydantic import SecretStr

from keyrag.config.types import Documents
from keyrag.embed.hasher import Hasher


def get_secret_from_env(env_var: str) -> SecretStr:
    """Get a secret from an environment variable."""
    return secret_from_env(env_var)()


def get_document_id(document: Document) -> str:
    """Get document id, as an hash of the document content and metadata."""
    hasher = Hasher(document.page_content)
    document_id = hasher.update(document.metadata)
    return document_id


def get_document_ids(
    documents: Documents,
    id_in_metadata: str | None = None,
) -> list[str]:
    """Get document ids, as an existing metadata field or hash of the document content and metadata.

    Args:
        documents (list[Document]): the list of documents.
        id_in_metadata (str, optional): the metadata field to use as id.
            When None, the id is an hash of the document content and metadata.
            Defaults to None.
    """
    if id_in_metadata is None:
        return [get_document_id(doc) for doc in documents]
    return [doc.metadata[id_in_metadata] for doc in documents]
