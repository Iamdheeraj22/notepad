import tkinter as tk
from tkinter import ttk
from models.document_statistics import DocumentStatistics

class StatusBar(ttk.Frame):
    """
    UI Component responsible for displaying the document status, such as
    counts, cursor position, encoding, and zoom level. It remains agnostic 
    of how the metrics are calculated and relies entirely on external 
    updates through `update_statistics`.
    """
    def __init__(self, parent: tk.Widget, on_zoom_selected=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.on_zoom_selected = on_zoom_selected
        
        # Configure the layout and appearance of the Status Bar
        self.config(relief=tk.SUNKEN, padding=(2, 2))
        
        # Define Tkinter StringVars to hold data for the labels
        self.position_var = tk.StringVar(value="Ln 1, Col 1")
        self.count_var = tk.StringVar(value="0 chars, 0 words")
        self.zoom_var = tk.StringVar(value="100%")
        self.line_ending_var = tk.StringVar(value="CRLF")
        self.encoding_var = tk.StringVar(value="UTF-8")
        self.mode_var = tk.StringVar(value="INS")
        self.modified_var = tk.StringVar(value="Saved")
        
        self._create_widgets()
        
    def _create_widgets(self):
        """
        Creates and packs the status bar labels. Layout typically goes 
        from right to left for system indicators, and left to right for counts.
        """
        # Encoding
        ttk.Separator(self, orient=tk.VERTICAL).pack(side=tk.RIGHT, fill=tk.Y, padx=2)
        ttk.Label(self, textvariable=self.encoding_var, width=10, anchor=tk.CENTER).pack(side=tk.RIGHT, padx=5)
        
        # Line Ending
        ttk.Separator(self, orient=tk.VERTICAL).pack(side=tk.RIGHT, fill=tk.Y, padx=2)
        ttk.Label(self, textvariable=self.line_ending_var, width=8, anchor=tk.CENTER).pack(side=tk.RIGHT, padx=5)
        
        # Zoom Percentage (Interactive Menubutton)
        ttk.Separator(self, orient=tk.VERTICAL).pack(side=tk.RIGHT, fill=tk.Y, padx=2)
        
        self.zoom_menu_btn = ttk.Menubutton(self, textvariable=self.zoom_var, width=6)
        self.zoom_menu_btn.pack(side=tk.RIGHT, padx=5)
        
        # Create the dropdown menu for Zoom
        self.zoom_menu = tk.Menu(self.zoom_menu_btn, tearoff=0)
        self.zoom_menu_btn["menu"] = self.zoom_menu
        
        # Populate with options 50% to 400%
        zoom_options = [50, 75, 100, 125, 150, 175, 200, 250, 300, 400]
        for z in zoom_options:
            self.zoom_menu.add_command(label=f"{z}%", command=lambda val=z: self._on_zoom_click(val))
        
        # Cursor Position
        ttk.Separator(self, orient=tk.VERTICAL).pack(side=tk.RIGHT, fill=tk.Y, padx=2)
        ttk.Label(self, textvariable=self.position_var, width=15, anchor=tk.CENTER).pack(side=tk.RIGHT, padx=5)

        # Insert/Overwrite Mode
        ttk.Separator(self, orient=tk.VERTICAL).pack(side=tk.RIGHT, fill=tk.Y, padx=2)
        ttk.Label(self, textvariable=self.mode_var, width=5, anchor=tk.CENTER).pack(side=tk.RIGHT, padx=5)
        
        # Document State (Modified/Saved)
        ttk.Separator(self, orient=tk.VERTICAL).pack(side=tk.RIGHT, fill=tk.Y, padx=2)
        ttk.Label(self, textvariable=self.modified_var, width=10, anchor=tk.CENTER).pack(side=tk.RIGHT, padx=5)
        
        # Document Counts (packed on the left side)
        ttk.Label(self, textvariable=self.count_var, anchor=tk.W).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
    def update_statistics(self, stats: DocumentStatistics):
        """
        Updates the UI labels using the provided DocumentStatistics object.
        Call this method whenever the document state changes (e.g., on keystrokes).
        """
        self.position_var.set(f"Ln {stats.current_line}, Col {stats.current_column}")
        self.count_var.set(f"{stats.char_count} chars, {stats.word_count} words, {stats.line_count} lines")
        if stats.zoom_percentage is not None:
            self.zoom_var.set(f"{stats.zoom_percentage}%")
            
        self.line_ending_var.set(stats.line_ending)
        self.encoding_var.set(stats.encoding)
        self.mode_var.set("INS" if stats.insert_mode else "OVR")
        self.modified_var.set("Modified" if stats.is_modified else "Saved")
            
    def _on_zoom_click(self, percentage):
        """Called when a zoom level is selected from the menu."""
        if self.on_zoom_selected:
            self.on_zoom_selected(percentage)
