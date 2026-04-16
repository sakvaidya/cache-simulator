"""
Manual verification of FIFO eviction order.
Run with:  python tests/test_fifo.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cache import Cache
from replacement import FIFOPolicy


def test_fifo_basic():
    # 4-way, 1 set => all blocks in set 0
    cache = Cache(cache_size=4, associativity=4, policy_name="FIFO")
    cache.set_policy(FIFOPolicy())

    for addr in [10, 20, 30, 40]:
        result, si, bi = cache.access(addr, "T")
        print(f"  Access {addr}: {result} -> set={si}, block={bi}")

    # Access 10 again — should NOT affect FIFO order
    cache.access(10, "T")
    print("  Accessed 10 again (FIFO should still evict 10 next)")

    # Next insert should evict 10 (first in)
    result, si, bi = cache.access(50, "T")
    tags_in_set = [b.tag for b in cache.sets[si].blocks]
    assert 10 not in tags_in_set, f"10 should have been evicted, got {tags_in_set}"
    print(f"  Access 50: {result} — 10 correctly evicted. Tags now: {tags_in_set}")
    print("  FIFO test PASSED!")


if __name__ == "__main__":
    test_fifo_basic()
