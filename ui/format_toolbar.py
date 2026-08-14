from tkinter import *
from tkinter import ttk
from tkinter import font
from services.format_service import FormatService

class FormatToolbar:
    def __init__(self, root: Tk, format_service: FormatService):
        self.root = root
        self.format_service = format_service
        self.toolbar_frame = None
        self.dialog = None

    def show(self):
        if self.dialog and self.dialog.winfo_exists():
            if self.dialog.state() == "withdrawn":
                self.dialog.deiconify()
            self.dialog.lift()
            self.dialog.focus_force()
            
            # Sync UI state with format_service
            self.font_family_var.set(self.format_service.current_family)
            self.font_size_var.set(str(self.format_service.current_size))
            self.wrap_var.set(self.format_service.current_wrap)
            self.auto_save_var.set(self.format_service.current_auto_save)
            return
            
        self.dialog = Toplevel(self.root)
        self.dialog.title("Format")
        self.dialog.resizable(False, False)
        self.dialog.transient(self.root)
        
        self.toolbar_frame = ttk.Frame(self.dialog, padding=10)
        self.toolbar_frame.pack(fill=BOTH, expand=True)
        
        # Font Settings
        font_frame = ttk.LabelFrame(self.toolbar_frame, text="Font Settings")
        font_frame.pack(side=TOP, fill=X, pady=5, padx=5)
        
        font_families = list(font.families())
        font_families.sort()
        
        self.font_family_var = StringVar(value=self.format_service.current_family)
        self.font_family_cb = ttk.Combobox(
            font_frame, 
            textvariable=self.font_family_var, 
            values=font_families,
            state="readonly",
            width=20
        )
        self.font_family_cb.pack(side=LEFT, padx=5, pady=5)
        self.font_family_cb.bind("<<ComboboxSelected>>", self.on_font_family_change)
        
        sizes = [8, 9, 10, 11, 12, 14, 16, 18, 20, 22, 24, 26, 28, 36, 48, 72]
        self.font_size_var = StringVar(value=str(self.format_service.current_size))
        self.font_size_cb = ttk.Combobox(
            font_frame,
            textvariable=self.font_size_var,
            values=sizes,
            width=4
        )
        self.font_size_cb.pack(side=LEFT, padx=5, pady=5)
        self.font_size_cb.bind("<<ComboboxSelected>>", self.on_font_size_change)
        self.font_size_cb.bind("<Return>", self.on_font_size_change) # handle manual entry
        
        # Wrap Settings
        self.wrap_var = BooleanVar(value=self.format_service.current_wrap)
        self.chk_wrap = ttk.Checkbutton(
            self.toolbar_frame, 
            text="Enable Word Wrap", 
            variable=self.wrap_var, 
            command=self.on_wrap_change
        )
        self.chk_wrap.pack(side=TOP, anchor=W, pady=5, padx=5)
        
        # Auto-Save Settings
        self.auto_save_var = BooleanVar(value=self.format_service.current_auto_save)
        self.chk_auto_save = ttk.Checkbutton(
            self.toolbar_frame, 
            text="Enable Auto-Save", 
            variable=self.auto_save_var, 
            command=self.on_auto_save_change
        )
        self.chk_auto_save.pack(side=TOP, anchor=W, pady=5, padx=5)
        
        # Action Buttons
        action_frame = ttk.Frame(self.toolbar_frame)
        action_frame.pack(side=TOP, fill=X, pady=10, padx=5)
        
        self.btn_save = ttk.Button(action_frame, text="Save", command=self.on_save_settings)
        self.btn_save.pack(side=LEFT, padx=5)

        self.btn_reset = ttk.Button(action_frame, text="Clear Format", command=self.format_service.reset_formatting)
        self.btn_reset.pack(side=RIGHT, padx=5)

    def on_save_settings(self):
        self.format_service.save_settings()
        if self.dialog:
            self.dialog.withdraw()
            
        # Restore focus to the editor so the user can continue typing
        if self.root:
            self.root.focus_force()
        if self.format_service.editor and self.format_service.editor.editor_widget:
            self.format_service.editor.editor_widget.focus_set()

    def on_wrap_change(self):
        self.format_service.set_word_wrap(self.wrap_var.get())

    def on_auto_save_change(self):
        self.format_service.set_auto_save(self.auto_save_var.get())

    def on_font_family_change(self, event=None):
        family = self.font_family_var.get()
        self.format_service.apply_font_family(family)

    def on_font_size_change(self, event=None):
        try:
            size = int(self.font_size_var.get())
            self.format_service.apply_font_size(size)
        except ValueError:
            pass # Invalid size entered
