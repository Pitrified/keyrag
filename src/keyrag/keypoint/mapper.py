"""Map documents to keypoints."""

import json
from pathlib import Path

from keyrag.utils.pathlib_ import check_create_fol


class Mapper:
    """Map documents to keypoints."""

    def __init__(
        self,
        cache_fol: Path,
    ) -> None:
        """Initialize the mapper."""
        self.cache_fol = cache_fol
        self.cache_fp = self.cache_fol / "mapper.json"
        self.load_data()

    def load_data(self) -> None:
        """Load the mapper data."""
        if self.cache_fp.exists():
            self.data = self.load_cache()
        else:
            self.data = {}

    def load_cache(self) -> dict[str, dict[str, float]]:
        """Load the cache."""
        return json.loads(self.cache_fp.read_text())

    def save_cache(self) -> None:
        """Save the cache."""
        check_create_fol(self.cache_fol)
        self.cache_fp.write_text(json.dumps(self.data, indent=2))

    def add_pair(
        self,
        doc_id: str,
        keypoint_id: str,
        similarity: float,
        auto_save: bool = True,
    ) -> None:
        """Add a pair to the mapper."""
        if keypoint_id not in self.data:
            self.data[keypoint_id] = {}
        self.data[keypoint_id][doc_id] = similarity
        if auto_save:
            self.save_cache()

    def get_similar_docs(
        self,
        keypoint_id: str,
        top_k: int,
    ) -> dict[str, float]:
        """Get similar documents."""
        # TODO optimize this
        # sort the documents by similarity
        return dict(
            sorted(self.data[keypoint_id].items(), key=lambda x: x[1], reverse=True)[
                :top_k
            ]
        )
