import tkinter as tk
from tkinter import ttk


class ConfigPanel(tk.Frame):
    def __init__(self, parent, on_update_config, **kwargs):
        super().__init__(parent, bg="#4a7c2f", **kwargs)
        self.on_update_config = on_update_config
        self._build()

    def _build(self):
        tk.Label(self, text="Cache Simulator", bg="#4a7c2f", fg="white",
                 font=("Helvetica", 13, "bold")).pack(pady=(10, 6))

        # Cache Size
        row = tk.Frame(self, bg="#4a7c2f")
        row.pack(fill=tk.X, padx=8, pady=2)
        tk.Label(row, text="Cache Size", bg="#4a7c2f", fg="white",
                 font=("Helvetica", 9)).pack(side=tk.LEFT)
        self.cache_size_var = tk.StringVar(value="16")
        ttk.Combobox(row, textvariable=self.cache_size_var,
                     values=["4", "8", "16", "32", "64"], width=5,
                     state="readonly").pack(side=tk.RIGHT)

        # Number of Sets
        row2 = tk.Frame(self, bg="#4a7c2f")
        row2.pack(fill=tk.X, padx=8, pady=2)
        tk.Label(row2, text="# Sets", bg="#4a7c2f", fg="white",
                 font=("Helvetica", 9)).pack(side=tk.LEFT)
        self.num_sets_var = tk.StringVar(value="4")
        ttk.Combobox(row2, textvariable=self.num_sets_var,
                     values=["1", "2", "4", "8"], width=5,
                     state="readonly").pack(side=tk.RIGHT)

        # Replacement Policy
        row3 = tk.Frame(self, bg="#4a7c2f")
        row3.pack(fill=tk.X, padx=8, pady=2)
        tk.Label(row3, text="Replacement Policy", bg="#4a7c2f", fg="white",
                 font=("Helvetica", 9)).pack(side=tk.LEFT)
        self.policy_var = tk.StringVar(value="RAND")
        ttk.Combobox(row3, textvariable=self.policy_var,
                     values=["RAND"], width=7,
                     state="readonly").pack(side=tk.RIGHT)

        ttk.Separator(self, orient="horizontal").pack(fill=tk.X, padx=8, pady=6)

    def get_config(self) -> dict:
        return {
            "cache_size": int(self.cache_size_var.get()),
            "num_sets": int(self.num_sets_var.get()),
            "policy": self.policy_var.get(),
        }
