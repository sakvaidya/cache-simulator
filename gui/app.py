import tkinter as tk
from cache import Cache
from replacement import RANDPolicy, LRUPolicy
from gui.config_panel import ConfigPanel
from gui.cache_view import CacheView, LegendBar


def make_policy(name: str):
    if name == "RAND":
        return RANDPolicy()
    elif name == "LRU":
        return LRUPolicy()
    raise ValueError(f"Unknown policy: {name}")


class App:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Cache Simulator")
        self.root.configure(bg="#4a7c2f")

        self.cache = None
        self.memory_refs = []
        self.ref_index = 0

        self.left_frame = tk.Frame(root, bg="#4a7c2f", width=260)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=6, pady=6)
        self.left_frame.pack_propagate(False)

        self.right_frame = tk.Frame(root, bg="white")
        self.right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=6, pady=6)

        self.config_panel = ConfigPanel(self.left_frame, on_update_config=self._on_update)
        self.config_panel.pack(fill=tk.X)

        self.cache_view = CacheView(self.right_frame)
        self.cache_view.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        self.legend = LegendBar(self.right_frame)
        self.legend.pack(fill=tk.X, padx=4, pady=(0, 4))

    def _on_update(self, cfg: dict):
        associativity = cfg["cache_size"] // cfg["num_sets"]
        self.cache = Cache(cfg["cache_size"], associativity, cfg["policy"])
        self.cache.set_policy(make_policy(cfg["policy"]))
        self.memory_refs = []
        self.ref_index = 0
        self.cache_view.setup(cfg["num_sets"], associativity)

    def step(self, address: int, task: str = "A"):
        if self.cache is None:
            return
        result, si, bi = self.cache.access(address, task)
        self.cache_view.refresh(self.cache, result, si, bi)
        return result, si, bi
