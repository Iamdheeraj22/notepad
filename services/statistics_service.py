import tkinter as tk
from models.document_statistics import DocumentStatistics

class DocumentStatisticsService:
    """
    Service responsible for inspecting the editor widget and computing
    all the necessary metrics (lines, words, characters, cursor position) 
    required for the Status Bar.
    """
    def __init__(self, editor_widget: tk.Text, zoom_service=None, document_state=None):
        self.editor_widget = editor_widget
        self.zoom_service = zoom_service
        self.document_state = document_state

    def calculate_statistics(self) -> DocumentStatistics:
        """
        Calculates the current statistics of the document based on the Text widget's content.
        """
        if not self.editor_widget:
            return DocumentStatistics()

        # Get all text from the widget (excluding the final newline Tkinter automatically adds)
        content = self.editor_widget.get("1.0", "end-1c")
        
        char_count = len(content)
        word_count = len(content.split())
        
        # Calculate line count based on the index of the end position
        line_count = int(self.editor_widget.index("end-1c").split(".")[0])
        
        # Determine cursor position
        cursor_index = self.editor_widget.index(tk.INSERT)
        current_line, current_column = map(int, cursor_index.split("."))
        current_column += 1  # Columns in Tkinter are 0-indexed, display as 1-indexed
        
        # Determine Insert/Overwrite mode 
        # By default, Tkinter text widgets are in insert mode, this can be tracked 
        # properly with key bindings in the editor, we default to True (INS) here.
        insert_mode = True 
        
        # Encoding and Line Endings would typically come from the FileService 
        # when a file is opened/saved. Hardcoded defaults for demonstration.
        encoding = "UTF-8"
        line_ending = "CRLF"
        
        # Zoom percentage tracked via the ZoomService
        zoom_percentage = self.zoom_service.get_zoom_percentage() if self.zoom_service else 100
        
        # Document modification state
        is_modified = self.document_state.is_modified if self.document_state else False

        return DocumentStatistics(
            word_count=word_count,
            char_count=char_count,
            line_count=line_count,
            current_line=current_line,
            current_column=current_column,
            insert_mode=insert_mode,
            encoding=encoding,
            line_ending=line_ending,
            zoom_percentage=zoom_percentage,
            is_modified=is_modified
        )
