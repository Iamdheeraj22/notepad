import os
import sys
from tkinter import *
from utils.constants import Constants as cs
from ui.editor import Editor as editor
from ui.menu import Menubar as menubar
from services.file_service import FileService
from services.shortcuts_service import ShortcutsService
from services.format_service import FormatService
from ui.format_toolbar import FormatToolbar
from models.document_state import DocumentState

class App:
    def __init__(self, config=None, resource_manager=None):
        from models.app_config import AppConfig
        self.config = config or AppConfig()
        
        # In a real scenario, this would have a fallback if none provided, 
        # but since we inject from main, we expect it.
        from services.resource_manager import ResourceManager
        self.resource_manager = resource_manager or ResourceManager()
        
        self.window = Tk()
        self.document_state = DocumentState()
        self.fileService = FileService(self.window, config=self.config)
        self.configureWindow()
        self.initializeUi()
        self.setup_auto_save()

    def configureWindow(self):
        self.update_title()
        
        #Height / Width
        self.window.minsize(width=800,height=500)
        self.window.geometry("800x500")
        
        icon = self.resource_manager.get_image("icon/icon2.png")
        if icon:
            self.window.iconphoto(False, icon)

    def initializeUi(self):
        from tkinter import ttk
        
        self.top_status_frame = ttk.Frame(self.window, relief=SUNKEN)
        
        self.top_status_var = StringVar(value="")
        self.top_status_label = ttk.Label(self.top_status_frame, textvariable=self.top_status_var, anchor=W)
        self.top_status_label.pack(side=LEFT, fill=X, expand=True, padx=5, pady=2)
        
        self.reset_search_btn = ttk.Button(self.top_status_frame, text="Reset", command=self.reset_search)
        self.reset_search_btn.pack(side=RIGHT, padx=5, pady=2)
        
        self.window.bind("<<SearchReplaceStatus>>", self.update_top_status)
        
        # Editor
        self.editor = editor(self.window, fileService=self.fileService, document_state=self.document_state, config=self.config)
        self.fileService.editor = self.editor
        
        self.formatService = FormatService(self.editor, config=self.config)
        
        # Zoom Service integration
        from services.zoom_service import ZoomService
        self.zoom_service = ZoomService(format_service=self.formatService, editor=self.editor)
        
        self.formatToolbar = FormatToolbar(self.window, self.formatService)
        
        menubar(self.window, fileService=self.fileService, editor=self.editor, formatToolbar=self.formatToolbar, zoomService=self.zoom_service).showMenu()
        
        self.editor.show()
        
        self.formatService.init_default_font()
        
        # Status Bar integration
        from services.statistics_service import DocumentStatisticsService
        from ui.status_bar import StatusBar
        
        self.stats_service = DocumentStatisticsService(self.editor.editor_widget, zoom_service=self.zoom_service, document_state=self.document_state)
        self.status_bar = StatusBar(self.window, on_zoom_selected=self.zoom_service.set_zoom, config=self.config)
        self.status_bar.pack(side=BOTTOM, fill=X)
        
        self.window.bind("<<UpdateStatus>>", self.update_status_bar)
        
        ShortcutsService(self.window,fileService=self.fileService, formatToolbar=self.formatToolbar).bindKeyboardsEvents()
        
        # Initial trigger
        self.update_status_bar()

    def update_top_status(self, event=None):
        search_str = getattr(self.editor, "last_search", "")
        replace_str = getattr(self.editor, "last_replace", None)
        
        if replace_str is not None:
            self.top_status_var.set(f"Find & Replace: '{search_str}' with '{replace_str}'")
            self.top_status_frame.pack(side=TOP, fill=X, before=self.editor.editor_frame)
        elif search_str:
            self.top_status_var.set(f"Searched: '{search_str}'")
            self.top_status_frame.pack(side=TOP, fill=X, before=self.editor.editor_frame)
        else:
            self.top_status_var.set("")
            self.top_status_frame.pack_forget()

    def reset_search(self):
        if hasattr(self, 'editor') and self.editor:
            self.editor.reset_search_replace()

    def update_status_bar(self, event=None):
        stats = self.stats_service.calculate_statistics()
        self.status_bar.update_statistics(stats)
        self.update_title()

    def update_title(self):
        fileName = self.fileService.getFileName()
        title = fileName if fileName else self.config.app_name
        if getattr(self, 'document_state', None) and self.document_state.is_modified:
            self.window.title(f"*{title}")
        else:
            self.window.title(title)

    def setup_auto_save(self):
        self.check_and_auto_save()

    def check_and_auto_save(self):
        # Schedule next check in 1000ms
        self.window.after(1000, self.check_and_auto_save)
        
        # Ensure formatService exists and auto-save is enabled
        if getattr(self, 'formatService', None) and self.formatService.current_auto_save:
            # Check if not untitled
            if self.fileService.getFileName() != "untitled" and self.fileService.getFileName() != "":
                # Check if modified
                if getattr(self, 'document_state', None) and self.document_state.is_modified:
                    self.fileService.save()

    def runApp(self):
        self.window.mainloop()
