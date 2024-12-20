"""Vector db that uses hash ids."""

import asyncio
from typing import Any, Coroutine

from langchain_chroma import Chroma
from langchain_core.documents import Document

from keyrag.config.types import Documents
from keyrag.utils.langchain_ import get_document_ids


class VectorDB(Chroma):
    """Vector db that uses hash ids."""

    def add_documents(
        self,
        documents: Documents,
        id_in_metadata: str | None = None,
        **kwargs: Any,
    ) -> list[str]:
        """Add documents, computing unique ids, unless provided in the metadata.

        Will only add documents that are not already in the database.

        Args:
            documents (list[Document]): List of documents to add.
            id_in_metadata (str, optional): the metadata field to use as id.
                When None, the id is an hash of the document content and metadata.
                Defaults to None.

        Returns:
            list[str]: List of ids of the newly added documents.
        """
        # filter new docs with ids
        new_ids, new_docs = self.filter_new_documents(
            documents=documents, id_in_metadata=id_in_metadata
        )
        # if there are no new documents, return an empty list
        if len(new_ids) == 0:
            return []
        # add the new documents, returning the ids
        return super().add_documents(documents=new_docs, ids=new_ids, **kwargs)

    async def aadd_documents(
        self,
        documents: Documents,
        id_in_metadata: str | None = None,
        **kwargs: Any,
    ) -> Coroutine[Any, Any, list[str]]:
        """Add documents, computing unique ids, unless provided in the metadata.

        Will only add documents that are not already in the database.

        Args:
            documents (list[Document]): List of documents to add.
            id_in_metadata (str, optional): the metadata field to use as id.
                When None, the id is an hash of the document content and metadata.
                Defaults to None.

        Returns:
            list[str]: List of ids of the newly added documents.
        """
        # filter new docs with ids
        new_ids, new_docs = self.filter_new_documents(
            documents=documents, id_in_metadata=id_in_metadata
        )
        # if there are no new documents, return an empty list
        if len(new_ids) == 0:
            return asyncio.sleep(0, result=[])
        return super().aadd_documents(documents=new_docs, ids=new_ids, **kwargs)

    def filter_new_documents(
        self,
        documents: Documents,
        id_in_metadata: str | None = None,
    ) -> tuple[list[str], Documents]:
        """Filter and keep only the new documents.

        Args:
            documents (list[Document]): List of documents to filter.
            id_in_metadata (str, optional): the metadata field to use as id.
                When None, the id is an hash of the document content and metadata.
                Defaults to None.

        Returns:
            tuple[list[str], Documents]: Tuple of the new ids and documents.
        """
        # get the ids of all the documents
        ids = get_document_ids(documents=documents, id_in_metadata=id_in_metadata)
        # get the ids of existing documents
        known_ids_data = self.get(ids=ids, include=[])
        known_ids: list[str] = known_ids_data["ids"]
        # filter and keep only the new ids and documents
        new_ids = [doc_id for doc_id in ids if doc_id not in known_ids]
        new_docs = [doc for doc, doc_id in zip(documents, ids) if doc_id in new_ids]
        return new_ids, new_docs
