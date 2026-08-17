import os
import tkinter as tk
from tkinter import ttk
from ui.dialogs.base_dialog import BaseDialog

class FileInfoDialog(BaseDialog):
    def __init__(self, parent, file_info):
        self.file_info = file_info
        super().__init__(parent, title="File Info")

    def create_body(self):
        body_frame = ttk.Frame(self, padding="20 20 20 0")
        body_frame.pack(fill="both", expand=True)

        row = 0
        for key, value in self.file_info.items():
            ttk.Label(body_frame, text=f"{key}:", font=("Helvetica", 10, "bold")).grid(row=row, column=0, sticky="e", padx=(0, 10), pady=5)
            if key == "File Path":
                val_entry = ttk.Entry(body_frame, width=45, font=("Helvetica", 10))
                val_entry.insert(0, str(value))
                val_entry.config(state="readonly")
                val_entry.grid(row=row, column=1, sticky="w", pady=5)
            else:
                val_label = ttk.Label(body_frame, text=str(value), font=("Helvetica", 10), wraplength=350)
                val_label.grid(row=row, column=1, sticky="w", pady=5)
            row += 1

    def create_buttons(self):
        button_frame = ttk.Frame(self, padding="0 10 20 20")
        button_frame.pack(fill="x")

        ttk.Button(
            button_frame,
            text="Close",
            command=self.on_ok
        ).pack(side="right")
