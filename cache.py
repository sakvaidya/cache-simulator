from dataclasses import dataclass, field
from typing import Optional, Tuple


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
        self.policy = None

        self.total_refs = 0
        self.hits = 0
        self.misses = 0
        self.reload_transients = 0
        self.last_access = None

    def set_policy(self, policy):
        self.policy = policy

    def get_set_index(self, address: int) -> int:
        return address % self.num_sets

    def get_tag(self, address: int) -> int:
        return address

    def access(self, address: int, task: str = "?") -> Tuple[str, int, int]:
        self.total_refs += 1
        set_index = self.get_set_index(address)
        tag = self.get_tag(address)
        cache_set = self.sets[set_index]

        for i, block in enumerate(cache_set.blocks):
            if block.valid and block.tag == tag:
                self.hits += 1
                self.policy.on_access(set_index, i)
                self.last_access = address
                return ("hit", set_index, i)

        self.misses += 1
        empty = next((i for i, b in enumerate(cache_set.blocks) if not b.valid), None)

        if empty is not None:
            idx = empty
        else:
            idx = self.policy.choose_victim(cache_set.blocks, set_index)

        result = "miss"
        if cache_set.blocks[idx].valid and cache_set.blocks[idx].tag == self.last_access:
            self.reload_transients += 1
            result = "reload_transient"

        cache_set.blocks[idx] = CacheBlock(tag=tag, valid=True, task=task)
        self.policy.on_insert(set_index, idx)
        self.last_access = address
        return (result, set_index, idx)

    def reset(self):
        self.sets = [CacheSet(self.associativity) for _ in range(self.num_sets)]
        self.total_refs = 0
        self.hits = 0
        self.misses = 0
        self.reload_transients = 0
        self.last_access = None
        if self.policy:
            self.policy.reset()

    @property
    def hit_rate(self) -> float:
        return self.hits / self.total_refs if self.total_refs else 0.0

    @property
    def miss_rate(self) -> float:
        return self.misses / self.total_refs if self.total_refs else 0.0
