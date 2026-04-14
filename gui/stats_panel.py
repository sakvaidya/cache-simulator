import tkinter as tk
import random


class MemRefBar(tk.Frame):
    """Horizontal bar showing the sequence of memory references."""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg="white", **kwargs)
        self.ref_labels = []

    def set_refs(self, refs: list, current_index: int = -1):
        for w in self.winfo_children():
            w.destroy()
        self.ref_labels = []

        tk.Label(self, text="Order of memory references after scheduling:",
                 bg="white", font=("Helvetica", 9, "bold")).pack(anchor="w", padx=6)

        bar = tk.Frame(self, bg="white")
        bar.pack(fill=tk.X, padx=6, pady=2)

        for i, ref in enumerate(refs):
            bg = "#00bcd4" if i <= current_index else "#b2ebf2"
            lbl = tk.Label(bar, text=str(ref), bg=bg, fg="white" if i <= current_index else "black",
                           font=("Helvetica", 9, "bold" if i == current_index else "normal"),
                           width=5, relief=tk.RIDGE, pady=4)
            lbl.pack(side=tk.LEFT, padx=1)
            self.ref_labels.append(lbl)

    def advance(self, index: int):
        for i, lbl in enumerate(self.ref_labels):
            if i < index:
                lbl.config(bg="#00bcd4", fg="white")
            elif i == index:
                lbl.config(bg="#0097a7", fg="white", font=("Helvetica", 9, "bold"))
            else:
                lbl.config(bg="#b2ebf2", fg="black", font=("Helvetica", 9, "normal"))


class ScrollableMemRefBar(tk.Frame):
    """Scrollable version of MemRefBar for long reference sequences."""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg="white", **kwargs)
        tk.Label(self, text="Order of memory references after scheduling:",
                 bg="white", font=("Helvetica", 9, "bold")).pack(anchor="w", padx=6)

        self.canvas = tk.Canvas(self, bg="white", height=36, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="horizontal",
                                       command=self.canvas.xview)
        self.canvas.configure(xscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.pack(side=tk.TOP, fill=tk.X)

        self.inner = tk.Frame(self.canvas, bg="white")
        self.canvas.create_window((0, 0), window=self.inner, anchor="nw")
        self.inner.bind("<Configure>",
                        lambda e: self.canvas.configure(
                            scrollregion=self.canvas.bbox("all")))
        self.ref_labels = []


import tkinter.ttk as ttk
