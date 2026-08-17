import tkinter as tk
from tkinter import font
from tkinter import colorchooser
import json
import os
from tkinter import colorchooser

class FormatService:
    def __init__(self, editor, config=None):
        self.editor = editor
        self.config = config
        self.font_cache = {}
        
        # Default font state
        self.current_family = self.config.default_font_family if self.config else "Arial"
        self.current_size = self.config.default_font_size if self.config else 12
        self.current_weight = "normal"
        self.current_slant = "roman"
        self.current_wrap = False
        self.current_auto_save = False
        self.current_zoom = self.config.default_zoom_percentage if self.config else 100
        self.settings_file = os.path.expanduser("~/.notepad_format_settings.json")
        
        self.load_settings()
        
        if self.editor and self.editor.editor_widget:
            self.init_default_font()

    def init_default_font(self):
        text_widget = self.editor.editor_widget
        effective_size = max(1, int(self.current_size * (self.current_zoom / 100)))
        default_font = font.Font(
            family=self.current_family, 
            size=effective_size,
            weight=self.current_weight,
            slant=self.current_slant
        )
        text_widget.configure(font=default_font)
        
        # Apply word wrap state on load
        new_wrap = tk.WORD if self.current_wrap else tk.NONE
        text_widget.configure(wrap=new_wrap)

    def load_settings(self):
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, "r") as f:
                    settings = json.load(f)
                    self.current_family = settings.get("family", "Arial")
                    self.current_size = settings.get("size", 12)
                    self.current_wrap = settings.get("wrap", False)
                    self.current_auto_save = settings.get("auto_save", False)
            except Exception as e:
                print(f"Error loading settings: {e}")
                
    def save_settings(self):
        settings = {
            "family": self.current_family,
            "size": self.current_size,
            "wrap": self.current_wrap,
            "auto_save": self.current_auto_save
        }
        try:
            with open(self.settings_file, "w") as f:
                json.dump(settings, f)
        except Exception as e:
            print(f"Error saving settings: {e}")
        
    def apply_font_family(self, family: str):
        self.current_family = family
        self._apply_current_font_state()

    def apply_font_size(self, size: int):
        self.current_size = size
        self._apply_current_font_state()
        
    def toggle_bold(self):
        if not self.editor or not self.editor.editor_widget: return
        
        if self.editor.editor_widget.tag_ranges(tk.SEL):
            current_tags = self.editor.editor_widget.tag_names(tk.SEL_FIRST)
            is_bold = any("_bold_" in t for t in current_tags)
            self.current_weight = "normal" if is_bold else "bold"
        else:
            self.current_weight = "normal" if self.current_weight == "bold" else "bold"
            
        self._apply_current_font_state()

    def toggle_italic(self):
        if not self.editor or not self.editor.editor_widget: return
        
        if self.editor.editor_widget.tag_ranges(tk.SEL):
            current_tags = self.editor.editor_widget.tag_names(tk.SEL_FIRST)
            is_italic = any("_italic" in t for t in current_tags)
            self.current_slant = "roman" if is_italic else "italic"
        else:
            self.current_slant = "roman" if self.current_slant == "italic" else "italic"
            
        self._apply_current_font_state()

    def toggle_underline(self):
        self._toggle_direct_tag("underline", "style_underline")

    def toggle_strikethrough(self):
        self._toggle_direct_tag("overstrike", "style_strikethrough")
        
    def _apply_current_font_state(self):
        if not self.editor or not self.editor.editor_widget:
            return
            
        text_widget = self.editor.editor_widget
        
        try:
            if text_widget.tag_ranges(tk.SEL):
                tag_name = f"font_{self.current_family}_{self.current_size}_{self.current_weight}_{self.current_slant}_{self.current_zoom}"
                
                if tag_name not in self.font_cache:
                    effective_size = max(1, int(self.current_size * (self.current_zoom / 100)))
                    new_font = font.Font(
                        family=self.current_family, 
                        size=effective_size,
                        weight=self.current_weight,
                        slant=self.current_slant
                    )
                    self.font_cache[tag_name] = new_font
                    text_widget.tag_configure(tag_name, font=new_font)
                    
                text_widget.tag_raise(tag_name)
                text_widget.tag_add(tag_name, tk.SEL_FIRST, tk.SEL_LAST)
        except Exception as e:
            print(f"Error applying font attribute: {e}")

    def _toggle_direct_tag(self, kwarg_key: str, tag_name: str):
        if not self.editor or not self.editor.editor_widget:
            return
            
        text_widget = self.editor.editor_widget
        
        try:
            if text_widget.tag_ranges(tk.SEL):
                current_tags = text_widget.tag_names(tk.SEL_FIRST)
                
                if tag_name in current_tags:
                    text_widget.tag_remove(tag_name, tk.SEL_FIRST, tk.SEL_LAST)
                else:
                    text_widget.tag_configure(tag_name, **{kwarg_key: True})
                    text_widget.tag_raise(tag_name)
                    text_widget.tag_add(tag_name, tk.SEL_FIRST, tk.SEL_LAST)
        except Exception as e:
            print(f"Error toggling tag {tag_name}: {e}")

    def apply_text_color(self):
        if not self.editor or not self.editor.editor_widget: return
        
        color = colorchooser.askcolor(title="Choose Text Color")
        if color[1]:
            self._apply_color_tag("foreground", color[1])
            
    def apply_bg_color(self):
        if not self.editor or not self.editor.editor_widget: return
        
        color = colorchooser.askcolor(title="Choose Highlight Color")
        if color[1]:
            self._apply_color_tag("background", color[1])
            
    def _apply_color_tag(self, kwarg_key: str, hex_color: str):
        if not self.editor or not self.editor.editor_widget:
            return
            
        text_widget = self.editor.editor_widget
        
        try:
            if text_widget.tag_ranges(tk.SEL):
                tag_name = f"color_{kwarg_key}_{hex_color}"
                
                text_widget.tag_configure(tag_name, **{kwarg_key: hex_color})
                text_widget.tag_raise(tag_name)
                text_widget.tag_add(tag_name, tk.SEL_FIRST, tk.SEL_LAST)
        except Exception as e:
            print(f"Error applying color tag {tag_name}: {e}")

    def set_word_wrap(self, enable: bool):
        self.current_wrap = enable
        if not self.editor or not self.editor.editor_widget: return
        text_widget = self.editor.editor_widget
        new_wrap = tk.WORD if enable else tk.NONE
        text_widget.configure(wrap=new_wrap)

    def set_auto_save(self, enable: bool):
        self.current_auto_save = enable

    def increase_indent(self):
        self._adjust_indent(20)

    def decrease_indent(self):
        self._adjust_indent(-20)

    def _adjust_indent(self, delta: int):
        if not self.editor or not self.editor.editor_widget: return
        text_widget = self.editor.editor_widget
        
        try:
            start = tk.SEL_FIRST + " linestart" if text_widget.tag_ranges(tk.SEL) else tk.INSERT + " linestart"
            end = tk.SEL_LAST + " lineend" if text_widget.tag_ranges(tk.SEL) else tk.INSERT + " lineend"
            
            current_tags = text_widget.tag_names(start)
            current_indent = 0
            for t in current_tags:
                if t.startswith("indent_"):
                    try:
                        current_indent = int(t.split("_")[1])
                    except:
                        pass
                        
            new_indent = max(0, current_indent + delta)
            tag_name = f"indent_{new_indent}"
            text_widget.tag_configure(tag_name, lmargin1=new_indent, lmargin2=new_indent)
            text_widget.tag_raise(tag_name)
            text_widget.tag_add(tag_name, start, end)
        except Exception as e:
            print(f"Error adjusting indent: {e}")

    def set_line_spacing(self, spacing: int):
        if not self.editor or not self.editor.editor_widget: return
        text_widget = self.editor.editor_widget
        
        try:
            start = tk.SEL_FIRST + " linestart" if text_widget.tag_ranges(tk.SEL) else tk.INSERT + " linestart"
            end = tk.SEL_LAST + " lineend" if text_widget.tag_ranges(tk.SEL) else tk.INSERT + " lineend"
            
            tag_name = f"spacing_{spacing}"
            text_widget.tag_configure(tag_name, spacing1=spacing, spacing2=spacing, spacing3=spacing)
            text_widget.tag_raise(tag_name)
            text_widget.tag_add(tag_name, start, end)
        except Exception as e:
            print(f"Error setting line spacing: {e}")

    def reset_formatting(self):
        if not self.editor or not self.editor.editor_widget: return
        text_widget = self.editor.editor_widget
        
        try:
            if text_widget.tag_ranges(tk.SEL):
                all_tags = text_widget.tag_names()
                for tag in all_tags:
                    if tag != "sel":
                        text_widget.tag_remove(tag, tk.SEL_FIRST, tk.SEL_LAST)
        except Exception as e:
            print(f"Error resetting formatting: {e}")

    def set_zoom(self, percentage: int):
        """
        Updates the active zoom multiplier and forces the font settings 
        to be recalculated and reapplied to the document.
        """
        self.current_zoom = percentage
        self.init_default_font()
        # Note: Depending on the app logic, we might also need to iterate 
        # through all existing font tags in the document and re-scale them, 
        # but for a simple notepad, setting the default font and adjusting the 
        # base style usually suffices unless there's mixed formatting.
        # For mixed formatting, we'd iterate over self.font_cache and re-configure them.
