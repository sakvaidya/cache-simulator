from dataclasses import dataclass, field
from typing import Optional


@dataclass
class CacheBlock:
    tag: Optional[int] = None
    valid: bool = False
    task: Optional[str] = None


@dataclass
class CacheSet:
    associativity: int = 1
    blocks: list = field(default_factory=list)

    def __post_init__(self):
        self.blocks = [CacheBlock() for _ in range(self.associativity)]


class Cache:
    def __init__(self, cache_size: int, associativity: int, policy_name: str = "RAND"):
        self.cache_size = cache_size
        self.associativity = associativity
        self.num_sets = cache_size // associativity
        self.sets = [CacheSet(associativity) for _ in range(self.num_sets)]
        self.policy_name = policy_name
        self.policy = None  # set after replacement.py is available

        # Statistics
        self.total_refs = 0
        self.hits = 0
        self.misses = 0
        self.reload_transients = 0
        self.last_access = None

    def get_set_index(self, address: int) -> int:
        return address % self.num_sets

    def reset(self):
        self.sets = [CacheSet(self.associativity) for _ in range(self.num_sets)]
        self.total_refs = 0
        self.hits = 0
        self.misses = 0
        self.reload_transients = 0
        self.last_access = None

    @property
    def hit_rate(self) -> float:
        if self.total_refs == 0:
            return 0.0
        return self.hits / self.total_refs

    @property
    def miss_rate(self) -> float:
        if self.total_refs == 0:
            return 0.0
        return self.misses / self.total_refs
