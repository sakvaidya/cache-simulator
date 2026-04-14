import tkinter as tk
from cache import Cache
from replacement import RANDPolicy, LRUPolicy
from gui.config_panel import ConfigPanel


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

        self.status = tk.Label(self.right_frame,
                               text="Configure cache and press 'Update Configuration'",
                               bg="white", font=("Helvetica", 11))
        self.status.pack(expand=True)

    def _on_update(self, cfg: dict):
        associativity = cfg["cache_size"] // cfg["num_sets"]
        self.cache = Cache(cfg["cache_size"], associativity, cfg["policy"])
        self.cache.set_policy(make_policy(cfg["policy"]))
        self.memory_refs = []
        self.ref_index = 0
        self.status.config(text=f"Cache ready: size={cfg['cache_size']}, "
                                f"sets={cfg['num_sets']}, policy={cfg['policy']}")
