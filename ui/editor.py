from tkinter import *
from tkinter import ttk
from services.file_service import FileService

class Editor():

    def __init__(self, root:Tk, fileService:FileService, document_state=None):
        self.root = root
        self.fileService = fileService
        self.document_state = document_state
        self.editor_widget = None

    def show(self):
        self.editor_frame = ttk.Frame(self.root)
        self.editor_frame.pack(fill=BOTH, expand=True)
        
        self.editor_widget = Text(
            self.editor_frame,
            width=1,
            height=1,
            padx=5,
            pady=5,
            border=0,
            borderwidth=0,
            highlightthickness=0,
            wrap='none',
            undo=True,
            autoseparators=True,
            maxundo=-1
        )

        ys = ttk.Scrollbar(self.editor_frame, orient='vertical', command=self.editor_widget.yview)
        xs = ttk.Scrollbar(self.editor_frame, orient='horizontal', command=self.editor_widget.xview)
        self.editor_widget.configure(yscrollcommand=ys.set, xscrollcommand=xs.set)

        ys.pack(side=RIGHT, fill=Y)
        xs.pack(side=BOTTOM, fill=X)
        self.editor_widget.pack(side=LEFT, fill=BOTH, expand=TRUE, padx=5, pady=5)
        
        # Bind events that change the document state or cursor position
        self.editor_widget.bind("<<Modified>>", self.trigger_status_update)
        self.editor_widget.bind("<KeyRelease>", self.trigger_status_update)
        self.editor_widget.bind("<ButtonRelease-1>", self.trigger_status_update)
        self.editor_widget.bind("<<Paste>>", self.trigger_status_update_delayed)
        self.editor_widget.bind("<<Cut>>", self.trigger_status_update_delayed)

    def trigger_status_update(self, event=None):
        if self.document_state:
            self.document_state.is_modified = (self.fetchFileContent() != self.document_state.saved_content)
        self.editor_widget.event_generate("<<UpdateStatus>>")
        
    def trigger_status_update_delayed(self, event=None):
        self.editor_widget.after(10, self.trigger_status_update)

    def insertData(self):
        filePath = self.fileService.getFilePath()
        if not filePath:
            return
        try:
            with open(f"{filePath}/{self.fileService.getFileName()}", mode="r", encoding="utf-8") as f:
                    content = f.read()
        
            self.editor_widget.delete("1.0", END)
            self.editor_widget.insert(END, content)
            self.set_unmodified()

        except Exception as e:
            print(e)

    def fetchFileContent(self):
        if self.editor_widget is None:
            return ""
        return self.editor_widget.get('1.0','end-1c')

    def set_unmodified(self):
        if self.editor_widget:
            self.editor_widget.edit_modified(False)
        if self.document_state:
            self.document_state.saved_content = self.fetchFileContent()
            self.document_state.is_modified = False
        self.trigger_status_update()

    def show_find_dialog(self):
        if hasattr(self, "find_dialog") and self.find_dialog.winfo_exists():
            self.find_dialog.focus_set()
            return
            
        self.find_dialog = Toplevel(self.root)
        self.find_dialog.title("Find")
        self.find_dialog.transient(self.root)
        self.find_dialog.resizable(False, False)
        self.find_dialog.configure(padx=20, pady=20)
        
        ttk.Label(self.find_dialog, text="Search:").grid(row=0, column=0, padx=(0, 10), pady=(0, 10), sticky=E)
        search_entry = ttk.Entry(self.find_dialog, width=25)
        search_entry.grid(row=0, column=1, pady=(0, 10), sticky=W)
        search_entry.focus_set()
        
        def on_search():
            search_str = search_entry.get()
            self.perform_find(search_str)
            self.find_dialog.destroy()
            self.editor_widget.focus_force()
            
        def close_dialog():
            self.find_dialog.destroy()
            self.editor_widget.focus_force()
            
        self.find_dialog.protocol("WM_DELETE_WINDOW", close_dialog)
        
        btn_frame = ttk.Frame(self.find_dialog)
        btn_frame.grid(row=1, column=0, columnspan=2, pady=(10, 0))
        
        ttk.Button(btn_frame, text="Search", command=on_search).pack(side=LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=close_dialog).pack(side=LEFT, padx=5)

    def show_replace_dialog(self):
        if hasattr(self, "replace_dialog") and self.replace_dialog.winfo_exists():
            self.replace_dialog.focus_set()
            return
            
        self.replace_dialog = Toplevel(self.root)
        self.replace_dialog.title("Find & Replace")
        self.replace_dialog.transient(self.root)
        self.replace_dialog.resizable(False, False)
        self.replace_dialog.configure(padx=20, pady=20)
        
        ttk.Label(self.replace_dialog, text="Search:").grid(row=0, column=0, padx=(0, 10), pady=(0, 10), sticky=E)
        search_entry = ttk.Entry(self.replace_dialog, width=25)
        search_entry.grid(row=0, column=1, pady=(0, 10), sticky=W)
        search_entry.focus_set()
        
        ttk.Label(self.replace_dialog, text="Replace:").grid(row=1, column=0, padx=(0, 10), pady=(0, 10), sticky=E)
        replace_entry = ttk.Entry(self.replace_dialog, width=25)
        replace_entry.grid(row=1, column=1, pady=(0, 10), sticky=W)
        
        def on_replace():
            search_str = search_entry.get()
            replace_str = replace_entry.get()
            self.perform_replace(search_str, replace_str)
            self.replace_dialog.destroy()
            self.editor_widget.focus_force()
            
        def close_dialog():
            self.replace_dialog.destroy()
            self.editor_widget.focus_force()
            
        self.replace_dialog.protocol("WM_DELETE_WINDOW", close_dialog)
            
        btn_frame = ttk.Frame(self.replace_dialog)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=(10, 0))
        
        ttk.Button(btn_frame, text="Replace", command=on_replace).pack(side=LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=close_dialog).pack(side=LEFT, padx=5)

    def perform_find(self, search_str):
        self.last_search = search_str
        self.last_replace = None
        self.root.event_generate("<<SearchReplaceStatus>>")
        
        self.editor_widget.tag_remove('found', '1.0', END)
        if search_str:
            idx = '1.0'
            while True:
                idx = self.editor_widget.search(search_str, idx, nocase=1, stopindex=END)
                if not idx: break
                lastidx = '%s+%dc' % (idx, len(search_str))
                self.editor_widget.tag_add('found', idx, lastidx)
                idx = lastidx
            self.editor_widget.tag_config('found', foreground='white', background='blue')
            
    def perform_replace(self, search_str, replace_str):
        self.last_search = search_str
        self.last_replace = replace_str
        self.root.event_generate("<<SearchReplaceStatus>>")
        
        content = self.editor_widget.get("1.0", "end-1c")
        if search_str and search_str in content:
            new_content = content.replace(search_str, replace_str)
            self.editor_widget.delete("1.0", END)
            self.editor_widget.insert("1.0", new_content)
            self.trigger_status_update()

    def reset_search_replace(self):
        self.last_search = ""
        self.last_replace = None
        if self.editor_widget:
            self.editor_widget.tag_remove('found', '1.0', END)
        self.root.event_generate("<<SearchReplaceStatus>>")