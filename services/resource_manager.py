import os
import sys
from pathlib import Path
from tkinter import PhotoImage

class ResourceManager:
    def __init__(self):
        self._image_cache = {}
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            self.base_path = Path(sys._MEIPASS)
        except AttributeError:
            self.base_path = Path(os.path.abspath("."))
            
    def get_path(self, relative_path: str) -> Path:
        """Returns the absolute path to a resource."""
        return self.base_path / relative_path
        
    def get_image(self, relative_path: str) -> PhotoImage:
        """Loads and caches a PhotoImage from a relative path."""
        if relative_path in self._image_cache:
            return self._image_cache[relative_path]
            
        full_path = self.get_path(relative_path)
        if not full_path.exists():
            print(f"Warning: Resource not found at {full_path}")
            return None
            
        try:
            image = PhotoImage(file=str(full_path))
            self._image_cache[relative_path] = image
            return image
        except Exception as e:
            print(f"Error loading image {full_path}: {e}")
            return None
            
    def clear_cache(self):
        """Clears the image cache."""
        self._image_cache.clear()
