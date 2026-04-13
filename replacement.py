from abc import ABC, abstractmethod
from typing import List
import random
from collections import OrderedDict
from cache import CacheBlock


class ReplacementPolicy(ABC):
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
        pass

    def on_insert(self, set_index: int, block_index: int):
        pass

    def reset(self):
        pass


class LRUPolicy(ReplacementPolicy):
    """
    Least Recently Used replacement.
    Tracks access order per set using an OrderedDict.
    The first key is always the least recently used block index.
    """

    def __init__(self):
        self._order: dict[int, OrderedDict] = {}

    def _get_order(self, set_index: int) -> OrderedDict:
        if set_index not in self._order:
            self._order[set_index] = OrderedDict()
        return self._order[set_index]

    def choose_victim(self, blocks: List[CacheBlock], set_index: int) -> int:
        order = self._get_order(set_index)
        if order:
            lru_idx = next(iter(order))
            return lru_idx
        return 0  # fallback

    def on_access(self, set_index: int, block_index: int):
        order = self._get_order(set_index)
        if block_index in order:
            order.move_to_end(block_index)
        else:
            order[block_index] = True

    def on_insert(self, set_index: int, block_index: int):
        order = self._get_order(set_index)
        order[block_index] = True
        order.move_to_end(block_index)

    def reset(self):
        self._order.clear()
