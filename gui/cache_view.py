import tkinter as tk
from tkinter import ttk

COLOR_HIT = "#00bcd4"
COLOR_MISS = "#f44336"
COLOR_RELOAD = "#ff9800"
COLOR_EMPTY = "#f5f5f5"
COLOR_OCCUPIED = "#00bcd4"


class CacheView(tk.Frame):
    """
    Displays the cache as a 2D grid:
      rows = sets, columns = ways (associativity)
    """

    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg="white", **kwargs)
        self.num_sets = 0
        self.associativity = 0
        self._cells = []   # list of list of Labels
        self._build_empty()

    def _build_empty(self):
        for w in self.winfo_children():
            w.destroy()
        self._cells = []

        tk.Label(self, text="Cache Contents:", bg="white",
                 font=("Helvetica", 10, "bold")).grid(
            row=0, column=0, columnspan=10, sticky="w", padx=6, pady=(6, 2))

    def setup(self, num_sets: int, associativity: int):
        self.num_sets = num_sets
        self.associativity = associativity
        for w in self.winfo_children():
            w.destroy()
        self._cells = []

        tk.Label(self, text="Cache Contents:", bg="white",
                 font=("Helvetica", 10, "bold")).grid(
            row=0, column=0, columnspan=associativity + 1,
            sticky="w", padx=6, pady=(6, 2))

        # Header
        tk.Label(self, text="SET #", bg="#e0e0e0", relief=tk.RIDGE,
                 font=("Helvetica", 9, "bold"), width=6).grid(
            row=1, column=0, padx=1, pady=1, sticky="nsew")

        header_text = f"{associativity}-way set-associative  (cache size = {num_sets * associativity} blocks)"
        tk.Label(self, text=header_text, bg="#e0e0e0", relief=tk.RIDGE,
                 font=("Helvetica", 9), width=40).grid(
            row=1, column=1, columnspan=associativity,
            padx=1, pady=1, sticky="nsew")

        # Rows per set
        for s in range(num_sets):
            tk.Label(self, text=str(s), bg="white", relief=tk.RIDGE,
                     font=("Helvetica", 9), width=6).grid(
                row=s + 2, column=0, padx=1, pady=1, sticky="nsew")
            row_cells = []
            for w in range(associativity):
                lbl = tk.Label(self, text="", bg=COLOR_EMPTY,
                               relief=tk.RIDGE, width=14, height=2,
                               font=("Helvetica", 9))
                lbl.grid(row=s + 2, column=w + 1, padx=1, pady=1, sticky="nsew")
                row_cells.append(lbl)
            self._cells.append(row_cells)

    def refresh(self, cache, last_result=None, last_set=None, last_block=None):
        """Update displayed cell contents from current cache state."""
        for s, cache_set in enumerate(cache.sets):
            for b, block in enumerate(cache_set.blocks):
                lbl = self._cells[s][b]
                if block.valid:
                    text = f"{block.tag}\nTask: {block.task}"
                    bg = COLOR_OCCUPIED
                    if s == last_set and b == last_block:
                        if last_result == "hit":
                            bg = COLOR_HIT
                        elif last_result == "reload_transient":
                            bg = COLOR_RELOAD
                        else:
                            bg = COLOR_MISS
                    lbl.config(text=text, bg=bg)
                else:
                    lbl.config(text="", bg=COLOR_EMPTY)
