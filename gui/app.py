import tkinter as tk
import random
from cache import Cache
from replacement import RANDPolicy, LRUPolicy, FIFOPolicy
from gui.config_panel import ConfigPanel, TaskPanel
from gui.cache_view import CacheView, LegendBar
from gui.stats_panel import MemRefBar


def make_policy(name: str):
    if name == "RAND":
        return RANDPolicy()
    elif name == "LRU":
        return LRUPolicy()
    elif name == "FIFO":
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

        # Left panel widgets
        self.config_panel = ConfigPanel(self.left_frame, on_update_config=self._on_update)
        self.config_panel.pack(fill=tk.X)

        self.task_panel = TaskPanel(self.left_frame)
        self.task_panel.pack(fill=tk.X, padx=6, pady=4)

        tk.Button(self.left_frame, text="Generate Memory References",
                  command=self._generate_refs,
                  bg="#2d5a1b", fg="white", relief=tk.FLAT,
                  padx=4, pady=4).pack(pady=2, fill=tk.X, padx=8)

        # Right panel widgets
        self.ref_bar = MemRefBar(self.right_frame)
        self.ref_bar.pack(fill=tk.X, padx=4, pady=(4, 0))

        self.cache_view = CacheView(self.right_frame)
        self.cache_view.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        self.legend = LegendBar(self.right_frame)
        self.legend.pack(fill=tk.X, padx=4, pady=(0, 4))

    def _on_update(self, cfg: dict):
        self._cfg = cfg
        associativity = cfg["cache_size"] // cfg["num_sets"]
        self.cache = Cache(cfg["cache_size"], associativity, cfg["policy"])
        self.cache.set_policy(make_policy(cfg["policy"]))
        self.memory_refs = []
        self.ref_index = 0
        self.cache_view.setup(cfg["num_sets"], associativity)

    def _generate_refs(self):
        task_cfg = self.task_panel.get_task_config()
        self.task_name = task_cfg["task_name"]
        n = task_cfg["num_refs"]
        pool = list(range(1, 32))
        self.memory_refs = [random.choice(pool) for _ in range(n)]
        self.ref_index = 0
        self.ref_bar.set_refs(self.memory_refs)

    def step(self, address: int = None, task: str = None):
        if self.cache is None:
            return
        if address is None:
            if self.ref_index >= len(self.memory_refs):
                return
            address = self.memory_refs[self.ref_index]
        result, si, bi = self.cache.access(address, task or self.task_name)
        self.cache_view.refresh(self.cache, result, si, bi)
        self.ref_bar.advance(self.ref_index)
        self.ref_index += 1
        return result, si, bi
