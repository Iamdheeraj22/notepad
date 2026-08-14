from tkinter import *
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

    def showMenu(self):
        self.configMenu()
    
