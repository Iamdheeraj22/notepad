from tkinter import *
import os
import time
from services.file_service import FileService

class Menubar():

    def __init__(self, root:Tk, fileService:FileService, editor=None, formatToolbar=None, zoomService=None):
        self.root = root
        self.fService = fileService
        self.editor = editor
        self.formatToolbar = formatToolbar
        self.zoomService = zoomService
        self.mainMenu = Menu()

    def configMenu(self):
        self.root.config(menu=self.mainMenu)
        self.configFileMenu()
        self.configEditMenu()
        self.configViewMenu()
        self.configInfoMenu()

    def configFileMenu(self):
        fileMenu = Menu(self.mainMenu)
        self.mainMenu.add_cascade(label="File", menu=fileMenu)
        fileMenuList = [
            {"mTitle":"New", "command":"newFile"},
            {"mTitle":"Open...", "command":"openFile"}, 
            {"mTitle":"Open Recents", "command":"openRecents"},
            {"mTitle":"Save", "command":"save"}, 
            {"mTitle":"Save As...", "command":"saveAs"}, 
            # {"mTitle":"Save All", "command":"saveAll"},
            # {"mTitle":"Close", "command":"close"}, 
            # {"mTitle":"Export", "command":"export"}, 
            # {"mTitle":"Print", "command":"print"}, 
            # {"mTitle":"Print Preview", "command":"printPreview"},
            {"mTitle":"Exit", "command":"exit"}
        ]

        for item in fileMenuList:
            title = item["mTitle"]
            if item["command"] == "openFile":
                fileMenu.add_command(label=title, command=self.open_file)
            else:
                fileMenu.add_command(label=title, command=getattr(self.fService, item["command"]))

        formatMenu = Menu(self.mainMenu)
        self.mainMenu.add_cascade(label="Format", menu=formatMenu)
        formatMenu.add_command(label="Font Settings", command=self.open_format_dialog)

    def open_format_dialog(self):
        if self.formatToolbar:
            self.formatToolbar.show()

    def configEditMenu(self):
        editMenu = Menu(self.mainMenu)
        self.mainMenu.add_cascade(label="Edit", menu=editMenu)
        if self.editor:
            editMenu.add_command(label="Find", command=self.editor.show_find_dialog)
            editMenu.add_command(label="Find & Replace", command=self.editor.show_replace_dialog)

    def configViewMenu(self):
        viewMenu = Menu(self.mainMenu)
        self.mainMenu.add_cascade(label="View", menu=viewMenu)
        
        zoomMenu = Menu(viewMenu)
        viewMenu.add_cascade(label="Zoom", menu=zoomMenu)
        
        if self.zoomService:
            zoomMenu.add_command(label="Zoom In", command=self.zoomService.zoom_in)
            zoomMenu.add_command(label="Zoom Out", command=self.zoomService.zoom_out)
            zoomMenu.add_command(label="Reset Zoom", command=self.zoomService.reset_zoom)

    def open_file(self):
        opened = self.fService.openFile()
        if opened and self.editor:
            self.editor.insertData()

    def configInfoMenu(self):
        infoMenu = Menu(self.mainMenu)
        self.mainMenu.add_cascade(label="Info", menu=infoMenu)
        infoMenu.add_command(label="File Info", command=self.show_file_info)

    def show_file_info(self):
        from ui.dialogs.file_info_dialog import FileInfoDialog
        from tkinter import messagebox
        
        file_name = self.fService.getFileName()
        file_path = self.fService.getFilePath()
        
        if not file_path or file_name == "untitled" or not file_name:
            messagebox.showwarning("Warning", "File information not showing until file is saved in the system.")
            return

        file_info = {
            "File Name": file_name,
            "File Path": "",
            "File Size": "",
            "Created Date": "",
            "Modified Date": "",
            "Read Only Status": "",
            "Encoding": ""
        }

        full_path = os.path.join(file_path, file_name)
        if os.path.exists(full_path):
            stat = os.stat(full_path)
            
            # File Path
            file_info["File Path"] = full_path
            
            # File Size
            size_kb = stat.st_size / 1024
            file_info["File Size"] = f"{size_kb:.2f} KB"
            
            # Dates
            created_time = time.localtime(stat.st_ctime)
            modified_time = time.localtime(stat.st_mtime)
            file_info["Created Date"] = time.strftime('%Y-%m-%d %H:%M:%S', created_time)
            file_info["Modified Date"] = time.strftime('%Y-%m-%d %H:%M:%S', modified_time)
            
            # Read Only Status
            is_read_only = not os.access(full_path, os.W_OK)
            file_info["Read Only Status"] = "Yes" if is_read_only else "No"
            
            # Encoding
            file_info["Encoding"] = "UTF-8" # editor.py defaults to utf-8

        dialog = FileInfoDialog(self.root, file_info)
        self.root.wait_window(dialog)

    def showMenu(self):
        self.configMenu()
    
