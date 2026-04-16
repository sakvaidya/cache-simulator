import tkinter as tk
from gui import App

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1000x620")
    app = App(root)
    root.mainloop()
