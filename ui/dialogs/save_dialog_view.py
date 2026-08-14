import tkinter as tk
from tkinter import ttk


class SaveFileDialog(tk.Toplevel):

    def __init__(self, parent,isSaveAs:bool=False):

        super().__init__(parent)
        self.isSaveAs=isSaveAs
        self.parent = parent
        self.result = None

        self.title("Save File" if not self.isSaveAs else "Save File As")
        self.geometry("420x220")
        self.resizable(False, False)

        self.transient(parent)
        self.grab_set()

        self.create_widgets()

        self.protocol("WM_DELETE_WINDOW", self.cancel)

    def create_widgets(self):

        container = ttk.Frame(self, padding=20)
        container.pack(fill="both", expand=True)

        # -------------------------
        # File Name
        # -------------------------

        ttk.Label(
            container,
            text="File Name"
        ).pack(anchor="w")

        self.file_name = ttk.Entry(
            container,
            width=40
        )

        self.file_name.pack(
            fill="x",
            pady=(5, 15)
        )

        self.file_name.focus()

        # -------------------------
        # File Type
        # -------------------------

        ttk.Label(
            container,
            text="File Type"
        ).pack(anchor="w")

        self.file_type = ttk.Combobox(
            container,
            state="readonly",
            values=[
                "Text File (*.txt)",
                "Python File (*.py)",
                "Markdown (*.md)",
                "JSON (*.json)",
                "HTML (*.html)",
                "All Files (*.*)"
            ]
        )

        self.file_type.current(0)

        self.file_type.pack(
            fill="x",
            pady=(5, 25)
        )

        # -------------------------
        # Buttons
        # -------------------------

        button_frame = ttk.Frame(container)
        button_frame.pack(anchor="e")

        ttk.Button(
            button_frame,
            text="Save",
            command=self.save
        ).pack(side="left", padx=5)

        ttk.Button(
            button_frame,
            text="Cancel",
            command=self.cancel
        ).pack(side="left")

    def save(self):

        self.result = {
            "filename": self.file_name.get().strip(),
            "filetype": self.file_type.get(),
            
        }
        self.destroy()

    def cancel(self):

        self.result = None
        self.destroy()