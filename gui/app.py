import random
import tkinter as tk

from cache import Cache
from gui.cache_view import CacheView, LegendBar
from gui.config_panel import ClockPanel, ConfigPanel, TaskPanel
from gui.stats_panel import MemRefBar, StatsPanel
from replacement import FIFOPolicy, LRUPolicy, RANDPolicy


def make_policy(name: str):
    if name == "RAND":
        return RANDPolicy()
    if name == "LRU":
        return LRUPolicy()
    if name == "FIFO":
        return FIFOPolicy()
    raise ValueError(f"Unknown policy: {name}")


class App:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Cache Simulator")
        self.root.configure(bg="#4a7c2f")

        self.cache = None
        self.memory_refs = []
        self.ref_index = 0
        self.task_name = "A"
        self._cfg = {}

        self.left_frame = tk.Frame(root, bg="#4a7c2f", width=260)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=6, pady=6)
        self.left_frame.pack_propagate(False)

        self.right_frame = tk.Frame(root, bg="white")
        self.right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=6, pady=6)

        self.config_panel = ConfigPanel(self.left_frame, on_update_config=self._on_update)
        self.config_panel.pack(fill=tk.X)

        self.task_panel = TaskPanel(self.left_frame)
        self.task_panel.pack(fill=tk.X, padx=6, pady=4)

        tk.Button(self.left_frame, text="Generate Memory References",
                  command=self._generate_refs,
                  bg="#2d5a1b", fg="white", relief=tk.FLAT,
                  padx=4, pady=4).pack(pady=2, fill=tk.X, padx=8)

        self.clock_panel = ClockPanel(
            self.left_frame,
            on_step=self._on_clock,
            on_reset=self._on_reset,
        )
        self.clock_panel.pack(fill=tk.X, pady=4)

        self.ref_bar = MemRefBar(self.right_frame)
        self.ref_bar.pack(fill=tk.X, padx=4, pady=(4, 0))

        self.cache_view = CacheView(self.right_frame)
        self.cache_view.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        self.legend = LegendBar(self.right_frame)
        self.legend.pack(fill=tk.X, padx=4, pady=(0, 2))

        self.stats_panel = StatsPanel(self.right_frame)
        self.stats_panel.pack(fill=tk.X, padx=4, pady=(0, 4))

    def _on_update(self, cfg: dict):
        self._cfg = cfg
        associativity = cfg["cache_size"] // cfg["num_sets"]
        self.cache = Cache(cfg["cache_size"], associativity, cfg["policy"])
        self.cache.set_policy(make_policy(cfg["policy"]))
        self.memory_refs = []
        self.ref_index = 0
        self.cache_view.setup(cfg["num_sets"], associativity)
        self.ref_bar.set_refs([])
        self.stats_panel.update_from_cache(self.cache)

    def _generate_refs(self):
        task_cfg = self.task_panel.get_task_config()
        self.task_name = task_cfg["task_name"]
        count = task_cfg["num_refs"]
        pool = list(range(1, 32))
        self.memory_refs = [random.choice(pool) for _ in range(count)]
        self.ref_index = 0
        self.ref_bar.set_refs(self.memory_refs)

    def _step_once(self):
        if self.cache is None or self.ref_index >= len(self.memory_refs):
            return False
        address = self.memory_refs[self.ref_index]
        result, set_index, block_index = self.cache.access(address, self.task_name)
        self.cache_view.refresh(self.cache, result, set_index, block_index)
        self.ref_bar.advance(self.ref_index)
        self.stats_panel.update_from_cache(self.cache, last_address=address)
        self.ref_index += 1
        return True

    def _on_clock(self, mode: str):
        if mode == "single":
            self._step_once()
        elif mode == "run":
            while self._step_once():
                pass

    def _on_reset(self):
        if self.cache:
            self.cache.reset()
            self.stats_panel.update_from_cache(self.cache)
        self.ref_index = 0
        if self._cfg:
            associativity = self._cfg["cache_size"] // self._cfg["num_sets"]
            self.cache_view.setup(self._cfg["num_sets"], associativity)
        self.ref_bar.set_refs(self.memory_refs)
