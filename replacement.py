from abc import ABC, abstractmethod
from collections import OrderedDict, deque
from typing import List
import random

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
    def choose_victim(self, blocks: List[CacheBlock], set_index: int) -> int:
        return random.randrange(len(blocks))

    def on_access(self, set_index: int, block_index: int):
        pass

    def on_insert(self, set_index: int, block_index: int):
        pass

    def reset(self):
        pass


class LRUPolicy(ReplacementPolicy):
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
        if block_index in order:
            order.move_to_end(block_index)
        else:
            order[block_index] = True

    def reset(self):
        self._order.clear()


class FIFOPolicy(ReplacementPolicy):
    def __init__(self):
        self._queue: dict[int, deque] = {}

    def _get_queue(self, set_index: int) -> deque:
        if set_index not in self._queue:
            self._queue[set_index] = deque()
        return self._queue[set_index]

    def choose_victim(self, blocks: List[CacheBlock], set_index: int) -> int:
        queue = self._get_queue(set_index)
        if queue:
            return queue[0]
        return 0

    def on_access(self, set_index: int, block_index: int):
        pass

    def on_insert(self, set_index: int, block_index: int):
        queue = self._get_queue(set_index)
        if block_index in queue:
            queue.remove(block_index)
        queue.append(block_index)

    def reset(self):
        self._queue.clear()
