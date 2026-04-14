from abc import ABC, abstractmethod
from typing import List
from cache import CacheBlock


class ReplacementPolicy(ABC):
    """Abstract base class for all cache replacement policies."""

    @abstractmethod
    def choose_victim(self, blocks: List[CacheBlock], set_index: int) -> int:
        """Return the index of the block to evict."""
        pass

    @abstractmethod
    def on_access(self, set_index: int, block_index: int):
        """Called on every cache access (hit or miss) for bookkeeping."""
        pass

    @abstractmethod
    def on_insert(self, set_index: int, block_index: int):
        """Called when a new block is inserted into the cache."""
        pass

    @abstractmethod
    def reset(self):
        """Reset internal policy state."""
        pass
