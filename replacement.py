from abc import ABC, abstractmethod
from typing import List
import random
from collections import OrderedDict, deque
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
    """Random replacement."""

    def choose_victim(self, blocks: List[CacheBlock], set_index: int) -> int:
        return random.randrange(len(blocks))

    def on_access(self, set_index: int, block_index: int):
        pass

    def on_insert(self, set_index: int, block_index: int):
        pass

    def reset(self):
        pass


class LRUPolicy(ReplacementPolicy):
    """Least Recently Used replacement."""

    def __init__(self):
        self._order: dict[int, OrderedDict] = {}

    def _get_order(self, set_index: int) -> OrderedDict:
        if set_index not in self._order:
            self._order[set_index] = OrderedDict()
        return self._order[set_index]

    def choose_victim(self, blocks: List[CacheBlock], set_index: int) -> int:
        order = self._get_order(set_index)
        if order:
            return next(iter(order))
        return 0

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


class FIFOPolicy(ReplacementPolicy):
    """
    First In First Out replacement.
    Tracks insertion order per set using a deque.
    The front of the deque is always the oldest (first-inserted) block index.
    """

    def __init__(self):
        self._queue: dict[int, deque] = {}

    def _get_queue(self, set_index: int) -> deque:
        if set_index not in self._queue:
            self._queue[set_index] = deque()
        return self._queue[set_index]

    def choose_victim(self, blocks: List[CacheBlock], set_index: int) -> int:
        q = self._get_queue(set_index)
        if q:
            return q[0]  # oldest inserted
        return 0

    def on_access(self, set_index: int, block_index: int):
        pass  # FIFO ignores accesses; only insertion order matters

    def on_insert(self, set_index: int, block_index: int):
        q = self._get_queue(set_index)
        # Remove if re-inserting (eviction replaced an existing slot)
        if block_index in q:
            q.remove(block_index)
        q.append(block_index)

    def reset(self):
        self._queue.clear()
