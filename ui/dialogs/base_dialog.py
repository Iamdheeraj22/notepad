import tkinter as tk
from tkinter import ttk


class BaseDialog(tk.Toplevel):

    def __init__(self, parent, title="Dialog"):

        super().__init__(parent)

        self.parent = parent

        self.title(title)

        self.resizable(False, False)

        self.transient(parent)

        self.grab_set()

        self.result = None

        self.create_body()

        self.create_buttons()

        self.center_window()

    def create_body(self):
        pass

    def create_buttons(self):

        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10)

        ttk.Button(
            button_frame,
            text="OK",
            command=self.on_ok
        ).pack(side="left", padx=5)

        ttk.Button(
            button_frame,
            text="Cancel",
            command=self.on_cancel
        ).pack(side="left")

    def on_ok(self):
        self.destroy()

    def on_cancel(self):
        self.result = None
        self.destroy()

    def center_window(self):

        self.update_idletasks()

        w = self.winfo_width()
        h = self.winfo_height()

        x = (self.winfo_screenwidth() // 2) - (w // 2)
        y = (self.winfo_screenheight() // 2) - (h // 2)

        self.geometry(f"+{x}+{y}")