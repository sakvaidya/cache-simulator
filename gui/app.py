import tkinter as tk
from tkinter import ttk


class App:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Cache Simulator")
        self.root.configure(bg="#4a7c2f")

        self.cache = None
        self.memory_refs = []
        self.ref_index = 0

        # Main layout: left panel | right panel
        self.left_frame = tk.Frame(root, bg="#4a7c2f", width=260)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=6, pady=6)
        self.left_frame.pack_propagate(False)

        self.right_frame = tk.Frame(root, bg="white")
        self.right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=6, pady=6)

        self._build_placeholder()

    def _build_placeholder(self):
        lbl = tk.Label(self.left_frame, text="Cache Simulator",
                       bg="#4a7c2f", fg="white",
                       font=("Helvetica", 13, "bold"))
        lbl.pack(pady=12)

        lbl2 = tk.Label(self.right_frame, text="Configure cache and press\n'Update Configuration'",
                        bg="white", font=("Helvetica", 11))
        lbl2.pack(expand=True)
