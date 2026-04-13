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
