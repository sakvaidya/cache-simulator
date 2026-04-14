from abc import ABC, abstractmethod
from typing import List
import random
from cache import CacheBlock


class ReplacementPolicy(ABC):
    """Abstract base class for all cache replacement policies."""

    @abstractmethod
    def choose_victim(self, blocks: List[CacheBlock], set_index: int) -> int:
        pass

    @abstractmethod
    def on_access(self, set_index: int, block_index: int):
        pass

    @abstractmethod
    def on_insert(self, set_index: int, block_index: int):
        pass

    @abstractmethod
    def reset(self):
        pass


class RANDPolicy(ReplacementPolicy):
    """Random replacement: evict a randomly chosen block."""

    def choose_victim(self, blocks: List[CacheBlock], set_index: int) -> int:
        return random.randrange(len(blocks))

    def on_access(self, set_index: int, block_index: int):
        pass  # RAND needs no bookkeeping

    def on_insert(self, set_index: int, block_index: int):
        pass

    def reset(self):
        pass
