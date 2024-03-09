from abc import ABC, abstractmethod
from typing import Any

from numpy import ndarray


class EmbeddingBuilder(ABC):
    def __init__(self, name: str, embedder: Any) -> None:
        self.name = name
        self.embedder = embedder

    @abstractmethod
    def embed(self, doc: str) -> ndarray:
        pass
