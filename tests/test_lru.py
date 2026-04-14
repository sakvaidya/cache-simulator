"""
Quick manual verification of LRU eviction order.
Run with:  python tests/test_lru.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cache import Cache
from replacement import LRUPolicy


def test_lru_basic():
    cache = Cache(cache_size=4, associativity=4, policy_name="LRU")
    cache.set_policy(LRUPolicy())

    for addr in [10, 20, 30, 40]:
        result, si, bi = cache.access(addr, "T")
        print(f"  Access {addr}: {result} -> set={si}, block={bi}")

    cache.access(10, "T")
    print("  Accessed 10 again (now MRU)")

    result, si, bi = cache.access(50, "T")
    tags_in_set = [b.tag for b in cache.sets[si].blocks]
    assert 20 not in tags_in_set, f"20 should have been evicted, got {tags_in_set}"
    print(f"  Access 50: {result} — 20 correctly evicted. Tags now: {tags_in_set}")
    print("  LRU test PASSED!")


if __name__ == "__main__":
    test_lru_basic()
