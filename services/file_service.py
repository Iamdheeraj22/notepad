import os
import tkinter.messagebox as mBox
from ui.dialogs.save_dialog_view import SaveFileDialog
from tkinter import filedialog as fd 
from tkinter import *
from utils.constants import Constants as cs
from tkinter.messagebox import *
import subprocess

class FileService():
    def __init__(self, *root: Tk, editor=None):
        self.currentFile = "untitled"
        self.currentFileName = ""
        self.currentFilePath = ""
        self.fileName = ""
        self.root = root[0] if root else None
        self.editor = editor

    def newFile(self):
        content_length = 0
        if self.editor:
            content = self.editor.fetchFileContent()
            content_length = len(content.strip())
            
        if self.currentFile == "untitled" and content_length == 0:
            return
            
        is_untitled = (self.currentFile == "untitled")
        
        self.save()
        
        if is_untitled and self.currentFile == "untitled":
            return
            
        self.currentFile = "untitled"
        self.currentFileName = ""
        self.currentFilePath = ""
        self.fileName = ""
        
        if self.root:
            self.root.title("untitled")
            
        if self.editor and self.editor.editor_widget:
            self.editor.editor_widget.delete("1.0", END)
            self.editor.set_unmodified()

    def openFile(self):
        name = fd.askopenfilename(
            defaultextension=["txt"], filetypes=cs.file_types
        )
        if not name:
            print("No file selected")
            return False
        self.fileName = name
        self.setFileDetails(
            isSavedFile=False,
            fullFilePath=""
        )
        if self.root:
            self.root.title(f"{self.getFileName()}")

        self.editor.insertData()
        return True


    def exit(self):
        resultValue = mBox.askyesno(
            title="Don't Save",
            message="Do you want to save your changes?",
            icon="warning",
            default="yes"
        )

        if resultValue:
            print("Yes")
        else:
            print("No")

    def openRecents(self):
        pass

    def save(self):
        if self.currentFile=="untitled":
            dialog=  SaveFileDialog(parent=self.root)
            self.root.wait_window(dialog)
            if dialog.result is None:
              print("Not saved")
              return

            #Save the file
            self.currentFileName = dialog.result["filename"]
            file_type = dialog.result["filetype"]

            extension=cs.FILE_TYPES[file_type]
            file_content = self.editor.fetchFileContent() if self.editor else ""
            with open(f"{self.currentFileName}{extension}",mode="x") as file:
                file.write(file_content)

            self.setFileDetails(
               True,
                fullFilePath=f"{self.currentFileName}{extension}"
            )            
        else:
            file_content = self.editor.fetchFileContent() if self.editor else ""
            full_path = os.path.join(self.currentFilePath, self.currentFile)
            with open(full_path, mode="w") as file:
                file.write(file_content)
                
        if self.editor:
            self.editor.set_unmodified()

    def saveAs(self):
        dialog = SaveFileDialog(parent=self.root,isSaveAs=True)
        self.root.wait_window(dialog)
        if dialog.result is None:
            print("Not saved")
            return

        #Save the file
        self.currentFileName = dialog.result["filename"]
        file_type = dialog.result["filetype"]

        extension = cs.FILE_TYPES[file_type]
        file_content = self.editor.fetchFileContent() if self.editor else ""
        
        with open(f"{self.currentFileName}{extension}", mode="w") as file:
            file.write(file_content)

        self.setFileDetails(
            True,
            fullFilePath=f"{self.currentFileName}{extension}"
        )
        if self.editor:
            self.editor.set_unmodified()

    def saveAll(self):
        print("Save All")
        pass

    def close(self):
        print("Close")
        pass

    def export(self):
        print("export")
        pass

    def print(self):
        contentLength=len(self.editor.fetchFileContent().strip())
        print("current file content length: ",contentLength)
        if self.currentFile=="untitled":
            if contentLength == 0:
                return
            result=mBox.askyesno(
                title="Save File",
                message="Do you want to save your changes?",
                icon="warning",
                default="yes"
            )

            if result:
                self.save()
                subprocess.run(["lp", self.getFilePath()])
            else:
                return
        else:
            file_content = self.editor.fetchFileContent() if self.editor else ""
            full_path = os.path.join(self.currentFilePath, self.currentFile)
            with open(full_path, mode="w") as file:
                file.write(file_content)
            subprocess.run(["open", "-a", "Preview", self.getFilePath()])

    def printPreview(self):
        print("Print Preview")
        pass

    def setFileDetails(self,isSavedFile:False,fullFilePath:str=""):
        if not isSavedFile:
            openFile = self.fileName
            self.currentFilePath = os.path.dirname(openFile)
            self.currentFile = os.path.basename(openFile)
            self.currentFileName = os.path.splitext(self.currentFile)[0]
        else:
            self.currentFilePath = os.path.dirname(fullFilePath)
            self.currentFile = os.path.basename(fullFilePath)
            self.currentFileName = os.path.splitext(self.currentFile)[0]
            if self.root:
                        self.root.title(f"{self.getFileName()}")

    def getFileName(self):
        return self.currentFile

    def getFilePath(self):
        return self.currentFilePath
