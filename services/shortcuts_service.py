from tkinter import *
from services import file_service as FileService
class ShortcutsService():
    def __init__(self,root:Tk,fileService:FileService, formatToolbar=None):
        self.rootWindow=root
        self.fileService=fileService
        self.formatToolbar=formatToolbar
        pass

    def bindKeyboardsEvents(self):
        self.rootWindow.bind("<Control-n>",func=lambda event: self.fileService.newFile())
        self.rootWindow.bind("<Control-o>", func=lambda event:self.fileService.openFile())
        self.rootWindow.bind("<Control-s>", func=lambda event:self.fileService.save())
        self.rootWindow.bind("<Control-Shift-S>", func=lambda event:self.fileService.saveAs())
        self.rootWindow.bind("<Control-p>", func=lambda event:self.fileService.print())
        self.rootWindow.bind("<Control-e>", func=lambda event:self.fileService.export())
        self.rootWindow.bind("<Control-q>",func=lambda event: quit())
        self.rootWindow.bind("<Control-f>", func=lambda event: self._open_format_dialog())
        def handle_find(event):
            if hasattr(self.fileService, "editor") and self.fileService.editor:
                self.fileService.editor.show_find_dialog()
            return "break"
            
        def handle_replace(event):
            if hasattr(self.fileService, "editor") and self.fileService.editor:
                self.fileService.editor.show_replace_dialog()
            return "break"

        self.rootWindow.bind("<Control-Shift-F>", handle_find)
        self.rootWindow.bind("<Control-Shift-R>", handle_replace)

    def _open_format_dialog(self):
        if self.formatToolbar:
            self.formatToolbar.show()