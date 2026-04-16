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

        row = tk.Frame(self, bg="#4a7c2f")
        row.pack(fill=tk.X, padx=8, pady=2)
        tk.Label(row, text="Cache Size", bg="#4a7c2f", fg="white",
                 font=("Helvetica", 9)).pack(side=tk.LEFT)
        self.cache_size_var = tk.StringVar(value="16")
        ttk.Combobox(row, textvariable=self.cache_size_var,
                     values=["4", "8", "16", "32", "64"], width=5,
                     state="readonly").pack(side=tk.RIGHT)

        row2 = tk.Frame(self, bg="#4a7c2f")
        row2.pack(fill=tk.X, padx=8, pady=2)
        tk.Label(row2, text="# Sets", bg="#4a7c2f", fg="white",
                 font=("Helvetica", 9)).pack(side=tk.LEFT)
        self.num_sets_var = tk.StringVar(value="4")
        ttk.Combobox(row2, textvariable=self.num_sets_var,
                     values=["1", "2", "4", "8"], width=5,
                     state="readonly").pack(side=tk.RIGHT)

        row3 = tk.Frame(self, bg="#4a7c2f")
        row3.pack(fill=tk.X, padx=8, pady=2)
        tk.Label(row3, text="Replacement Policy", bg="#4a7c2f", fg="white",
                 font=("Helvetica", 9)).pack(side=tk.LEFT)
        self.policy_var = tk.StringVar(value="RAND")
        ttk.Combobox(row3, textvariable=self.policy_var,
                     values=["RAND"], width=7,
                     state="readonly").pack(side=tk.RIGHT)

        ttk.Separator(self, orient="horizontal").pack(fill=tk.X, padx=8, pady=6)

        tk.Button(self, text="Update Configuration",
                  command=self._emit_update,
                  bg="#2d5a1b", fg="white",
                  relief=tk.FLAT, padx=6, pady=4).pack(pady=4)

    def _emit_update(self):
        self.on_update_config(self.get_config())

    def get_config(self) -> dict:
        return {
            "cache_size": int(self.cache_size_var.get()),
            "num_sets": int(self.num_sets_var.get()),
            "policy": self.policy_var.get(),
        }

    def set_available_policies(self, policies: list):
        """Called by other modules to register their policies."""
        for widget in self.winfo_children():
            if isinstance(widget, tk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, ttk.Combobox) and \
                       self.policy_var in (child.cget("textvariable"),):
                        child.configure(values=policies)


class TaskPanel(tk.Frame):
    """Panel for entering task name and number of memory references."""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg="#4a7c2f", **kwargs)
        self._build()

    def _build(self):
        tk.Label(self, text="Task Name", bg="#4a7c2f", fg="white",
                 font=("Helvetica", 9)).grid(row=0, column=0, sticky="w", padx=4, pady=2)
        self.task_name_var = tk.StringVar(value="task A")
        tk.Entry(self, textvariable=self.task_name_var, width=14).grid(
            row=0, column=1, padx=4, pady=2)

        tk.Label(self, text="# Memory Refs", bg="#4a7c2f", fg="white",
                 font=("Helvetica", 9)).grid(row=1, column=0, sticky="w", padx=4, pady=2)
        self.num_refs_var = tk.StringVar(value="8")
        tk.Entry(self, textvariable=self.num_refs_var, width=6).grid(
            row=1, column=1, padx=4, pady=2)

    def get_task_config(self) -> dict:
        return {
            "task_name": self.task_name_var.get(),
            "num_refs": int(self.num_refs_var.get()),
        }


class ClockPanel(tk.Frame):
    """Step/Run controls at the bottom of the left panel."""

    def __init__(self, parent, on_step, on_reset, **kwargs):
        super().__init__(parent, bg="#4a7c2f", **kwargs)
        self.on_step = on_step
        self.on_reset = on_reset
        self._build()

    def _build(self):
        tk.Label(self, text="Clock Options", bg="#4a7c2f", fg="white",
                 font=("Helvetica", 9, "bold")).pack(anchor="w", padx=6, pady=(6, 2))

        self.mode_var = tk.StringVar(value="single")
        modes = [("Single Step", "single"), ("Run to Completion", "run")]
        for text, val in modes:
            tk.Radiobutton(self, text=text, variable=self.mode_var, value=val,
                           bg="#4a7c2f", fg="white", selectcolor="#2d5a1b",
                           font=("Helvetica", 9)).pack(anchor="w", padx=12)

        btn_row = tk.Frame(self, bg="#4a7c2f")
        btn_row.pack(fill=tk.X, padx=8, pady=4)

        tk.Button(btn_row, text="Step/Run", command=self._on_step_run,
                  bg="#2d5a1b", fg="white", relief=tk.FLAT,
                  padx=8, pady=4).pack(side=tk.LEFT, padx=2)

        tk.Button(btn_row, text="Reset", command=self.on_reset,
                  bg="#8b0000", fg="white", relief=tk.FLAT,
                  padx=8, pady=4).pack(side=tk.LEFT, padx=2)

    def _on_step_run(self):
        self.on_step(self.mode_var.get())
